Where:
- **λ_i** = Force of infection (driven by contact matrix C_ij)
- **γ** = Recovery rate (1/10 days)
- **η_i** = Isolation/testing rate (age-dependent)
- **μ_i** = Case fatality rate (0.1%, 1%, 10% for Young/Adults/Elderly)
- **ξ** = Rate of immunity waning (1/90 days)
- **ψ_i(t)** = Vaccination rate (strategy-dependent)

### Contact Matrix

```python
C = [[10.0,  5.0,  1.0],   # Young mix heavily with Young
     [ 5.0,  8.0,  4.0],   # Adults mix with everyone
     [ 1.0,  4.0,  2.0]]   # Elderly are isolated
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/jdf0607/Epidemic_simulator
cd epidemic-vaccination-model
```

## 💻 Usage

### Run the Simulation

```bash
python main.py
```

This will:
1. Execute all three vaccination scenarios (None, Mortality, Transmission)
2. Generate interactive plots showing epidemic curves
3. Print final statistics to console

### Generate PDF Report

```bash
python report_generator.py
```

Outputs: `Lab11_Final_Report.pdf` with comprehensive analysis

### Customize Parameters

Edit `lab11_epidemics.py` to modify:

```python
# Population structure
POPULATION = np.array([30000, 50000, 20000])  # Young, Adults, Elderly

# Vaccination capacity
MAX_DOSES_PER_DAY = 500  # 0.5% of population
VACCINE_START_DAY = 50

# Disease parameters
BETA_BASE = 0.3          # Transmission rate
GAMMA = 1.0 / 10.0       # Recovery (10 days)
MU = np.array([0.001, 0.01, 0.1])  # Fatality rates
```

## 📈 Interpretation of Results

### Plot A: Active Infections (I + Q)
Shows epidemic curve dynamics. The "Elderly First" strategy doesn't flatten the curve as effectively as "Young First" but prevents deaths.

### Plot B: Cumulative Deaths
**Critical metric**: Demonstrates clear superiority of vulnerability-based prioritization under limited vaccine supply.

### Plot C: Infections by Group
Reveals how vaccination shifts infection burden between age groups.

### Plot D: Impact of NPIs
Combining mobility restrictions (β reduction) with vaccination delays the peak, maximizing vaccine coverage before surge.

## 🧪 Scientific Context

This model addresses a core **optimization problem in public health**:

> *Given limited vaccine doses, should we prioritize high-risk groups (direct protection) or high-contact groups (transmission blocking)?*

**Answer**: When fatality rates vary significantly by group (10% vs 0.1%), **direct protection dominates** despite higher residual transmission.

### Real-World Applications

- COVID-19 vaccination rollout strategies (2020-2021)
- Influenza vaccination in aging populations
- Resource allocation during emerging infectious diseases
- Policy evaluation for pandemic preparedness

## 🔬 Model Assumptions & Limitations

**Assumptions:**
- Homogeneous mixing within groups
- Perfect vaccine efficacy (100%)
- Deterministic dynamics (mean-field approximation)
- Fixed contact patterns throughout epidemic

**Limitations:**
- No spatial heterogeneity
- Simplified SIRS immunity (waning after 90 days)
- Does not model healthcare capacity constraints
- Ignores behavioral changes post-vaccination

## 📚 References

1. **Keeling & Rohani** (2008). *Modeling Infectious Diseases in Humans and Animals*
2. **Bubar et al.** (2021). "Model-informed COVID-19 vaccine prioritization strategies by age and serostatus." *Science*
3. **Mossong et al.** (2008). "Social contacts and mixing patterns relevant to the spread of infectious diseases." *PLoS Medicine*

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add stochastic implementation (Gillespie algorithm)
- [ ] Implement spatial network structure
- [ ] Include vaccine hesitancy dynamics
- [ ] Add economic cost-benefit analysis
- [ ] Support for custom disease parameters (GUI)



## 👥 Authors

- **José Duran**

## 🙏 Acknowledgments

- Computer Aided Simulations Lab course materials
- Public health modeling community
- SciPy/NumPy development teams

---
