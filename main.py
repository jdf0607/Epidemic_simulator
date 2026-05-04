import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# ==========================================
# 1. PARAMETERS & CONFIGURATION
# ==========================================

# Simulation Settings
DAYS = 200
DT = 1.0       # Time step (1 day)
GROUPS = 3     # 0: Young, 1: Adults, 2: Elderly
NAMES = ['Young', 'Adults', 'Elderly']
POPULATION = np.array([30000, 50000, 20000]) # Total 100k

# Disease Parameters
BETA_BASE = 0.3          # Base transmission rate
GAMMA = 1.0 / 10.0       # Recovery rate (10 days duration)
ETA = np.array([0.1, 0.2, 0.4]) # Isolation rate (Elderly tested more often)
MU = np.array([0.001, 0.01, 0.1]) # Fatality rate (High for Elderly)
XI = 1.0 / 90.0          # Immunity wanes after ~3 months (SIRS)

# Contact Matrix C[i,j]: Contact FROM i TO j
# Young mix with Young; Adults mix with everyone; Elderly isolated
CONTACT_MATRIX = np.array([
    [10.0, 5.0,  1.0], 
    [ 5.0, 8.0,  4.0], 
    [ 1.0, 4.0,  2.0]
])

# Vaccination Settings
VACCINE_START_DAY = 50
MAX_DOSES_PER_DAY = 500  # 0.5% of pop per day
VACCINE_EFFICACY = 1.0   # Perfect vaccine for simplicity

# ==========================================
# 2. MODEL ENGINE
# ==========================================

def deriv(y, t, beta, contact_mat):
    # Unpack state (flattened vector)
    # Structure: [S0..S2, I0..I2, Q0..Q2, R0..R2, V0..V2, D0..D2]
    k = GROUPS
    S = y[0:k]
    I = y[k:2*k]
    Q = y[2*k:3*k]
    R = y[3*k:4*k]
    
    # Calculate total living population for normalization
    N = POPULATION # Approximation (assuming deaths are small relative to N for force of infection)
    
    # Force of Infection (Lambda)
    # Lambda_i = Beta * Sum(C_ij * I_j / N_j)
    Lambda = np.zeros(k)
    for i in range(k):
        sum_contact = 0
        for j in range(k):
            sum_contact += contact_mat[i,j] * (I[j] / N[j])
        Lambda[i] = beta * sum_contact
    
    # Derivatives
    dSdt = -S * Lambda + XI * R
    dIdt = S * Lambda - GAMMA * I - ETA * I
    dQdt = ETA * I - GAMMA * Q - MU * Q
    dRdt = GAMMA * I + GAMMA * Q - XI * R
    dVdt = np.zeros(k) # Handled externally in the daily loop
    dDdt = MU * Q
    
    return np.concatenate([dSdt, dIdt, dQdt, dRdt, dVdt, dDdt])

def run_simulation(strategy_name="None", npi_factor=1.0):
    # Initial Conditions
    # Start with 10 infected in Group 1 (Adults)
    S = POPULATION.copy().astype(float)
    I = np.zeros(GROUPS); I[1] = 50 
    Q = np.zeros(GROUPS)
    R = np.zeros(GROUPS)
    V = np.zeros(GROUPS)
    D = np.zeros(GROUPS)
    
    S -= I # Remove initial infected from Susceptible
    
    # State Vector
    y = np.concatenate([S, I, Q, R, V, D])
    
    # History storage
    history = []
    times = np.arange(0, DAYS, DT)
    
    # === DAY BY DAY SIMULATION ===
    for day in range(len(times)-1):
        
        current_state = y
        
        # 1. Apply NPIs (Mobility Restrictions)
        # If infected > 1000, reduce Beta by NPI factor
        total_infected = np.sum(current_state[GROUPS:2*GROUPS])
        current_beta = BETA_BASE
        if total_infected > 1000:
             current_beta = BETA_BASE * npi_factor # E.g., 0.5 for 50% reduction
        
        # 2. Run ODE for 1 step
        t_step = [times[day], times[day+1]]
        sol = odeint(deriv, current_state, t_step, args=(current_beta, CONTACT_MATRIX))
        new_state = sol[-1]
        
        # 3. Apply Vaccination (Discrete Logic)
        if day >= VACCINE_START_DAY:
            # How many doses available?
            doses_left = MAX_DOSES_PER_DAY
            
            # Prioritization Logic
            priority_order = []
            
            if strategy_name == "Mortality": 
                # Vaccinate Elderly (2) -> Adults (1) -> Young (0)
                priority_order = [2, 1, 0]
            elif strategy_name == "Transmission": 
                # Vaccinate High Mixers: Young (0) -> Adults (1) -> Elderly (2)
                priority_order = [0, 1, 2]
            elif strategy_name == "None":
                priority_order = []
                
            # Distribute doses
            current_S = new_state[0:GROUPS]
            current_V = new_state[4*GROUPS:5*GROUPS]
            
            for grp_idx in priority_order:
                if doses_left <= 0: break
                
                # Can only vaccinate susceptible people
                candidates = current_S[grp_idx]
                if candidates > 0:
                    vaccinated_count = min(candidates, doses_left)
                    
                    # Update state manually
                    current_S[grp_idx] -= vaccinated_count
                    current_V[grp_idx] += vaccinated_count
                    doses_left -= vaccinated_count
            
            # Re-pack state
            new_state[0:GROUPS] = current_S
            new_state[4*GROUPS:5*GROUPS] = current_V

        # Save and Update
        history.append(new_state)
        y = new_state
        
    return np.array(history), times[:-1]

# ==========================================
# 3. RUN SCENARIOS & PLOT
# ==========================================

# Scenario 1: Protect Vulnerable (Mortality Strategy)
res_mort, t = run_simulation("Mortality", npi_factor=1.0)
# Scenario 2: Stop Spread (Transmission Strategy)
res_trans, _ = run_simulation("Transmission", npi_factor=1.0)
# Scenario 3: No Vaccine
res_none, _ = run_simulation("None", npi_factor=1.0)

# Helper to extract Total Deaths
def get_total_deaths(res):
    # Deaths are the last K elements of the state vector
    return np.sum(res[:, 5*GROUPS:6*GROUPS], axis=1)

def get_total_infected(res):
    # Undetected Infected + Quarantined (Active Cases)
    I_all = np.sum(res[:, GROUPS:2*GROUPS], axis=1)
    Q_all = np.sum(res[:, 2*GROUPS:3*GROUPS], axis=1)
    return I_all + Q_all

# Plotting
plt.figure(figsize=(12, 10))

# Plot A: Epidemic Curves (Active Cases)
plt.subplot(2, 2, 1)
plt.plot(t, get_total_infected(res_none), 'k--', label='No Vaccine')
plt.plot(t, get_total_infected(res_mort), 'r', label='Prioritize Elderly')
plt.plot(t, get_total_infected(res_trans), 'b', label='Prioritize Young')
plt.axvline(VACCINE_START_DAY, color='gray', linestyle=':', label='Vaccination Start')
plt.title("Active Infections (I + Q)")
plt.xlabel("Days")
plt.ylabel("People")
plt.legend()
plt.grid(True)

# Plot B: Cumulative Deaths
plt.subplot(2, 2, 2)
plt.plot(t, get_total_deaths(res_none), 'k--', label='No Vaccine')
plt.plot(t, get_total_deaths(res_mort), 'r', label='Prioritize Elderly')
plt.plot(t, get_total_deaths(res_trans), 'b', label='Prioritize Young')
plt.title("Cumulative Deaths")
plt.xlabel("Days")
plt.ylabel("Deaths")
plt.legend()
plt.grid(True)

# Plot C: Group Dynamics (Mortality Strategy)
# Show how different groups get infected in the 'Prioritize Elderly' case
plt.subplot(2, 2, 3)
idx_I_start = GROUPS
plt.plot(t, res_mort[:, idx_I_start+0], label='Young (I)', color='blue', alpha=0.6)
plt.plot(t, res_mort[:, idx_I_start+1], label='Adults (I)', color='orange', alpha=0.6)
plt.plot(t, res_mort[:, idx_I_start+2], label='Elderly (I)', color='red', alpha=0.6)
plt.title("Infections by Group (Strategy: Elderly First)")
plt.xlabel("Days")
plt.legend()
plt.grid(True)

# Plot D: Interaction with NPIs
# Let's run a case with Vaccine + NPI (Lockdown when cases > 1000)
res_npi, _ = run_simulation("Mortality", npi_factor=0.6) # 40% reduction in beta
plt.subplot(2, 2, 4)
plt.plot(t, get_total_infected(res_mort), 'r', label='Vaccine Only')
plt.plot(t, get_total_infected(res_npi), 'g', label='Vaccine + NPI (Lockdown)')
plt.title("Impact of NPIs during Vaccination")
plt.xlabel("Days")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Print Final Stats
print(f"Total Deaths (No Vaccine): {get_total_deaths(res_none)[-1]:.0f}")
print(f"Total Deaths (Strategy Elderly): {get_total_deaths(res_mort)[-1]:.0f}")
print(f"Total Deaths (Strategy Young): {get_total_deaths(res_trans)[-1]:.0f}")
