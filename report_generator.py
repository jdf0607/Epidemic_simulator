from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Logo placeholder (optional) or simplified header
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Lab 11: Multi-Group SIR-type Model & Vaccination Strategies', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Computer Aided Simulations Lab - Final Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(220, 220, 220) # Light grey
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

def create_final_report():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # --- 1. MODEL FORMULATION ---
    pdf.chapter_title('1. Model Formulation and Structure')
    pdf.chapter_body(
        "We formulated a Multi-Group SIQRS (Susceptible-Infected-Quarantined-Recovered-Susceptible) model "
        "to account for population inhomogeneity. The population is divided into K=3 groups: "
        "Group 0 (Young/Mobile), Group 1 (Adults), and Group 2 (Elderly/Vulnerable).\n\n"
        "The dynamics are governed by the following Mean-Field Equations for each group i:"
    )
    
    # Simple representation of ODEs
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 5, 
        "dS_i/dt = -S_i * Lambda_i + Xi * R_i - Psi_i(t)\n"
        "dI_i/dt = S_i * Lambda_i - Gamma * I_i - Eta_i * I_i\n"
        "dQ_i/dt = Eta_i * I_i - Gamma * Q_i - Mu_i * Q_i\n"
        "dD_i/dt = Mu_i * Q_i\n\n"
        "Where Lambda_i is the force of infection driven by the Contact Matrix C_ij."
    )
    pdf.ln(5)

    # --- 2. EXPERIMENTAL SETUP ---
    pdf.chapter_title('2. Experimental Setup')
    pdf.chapter_body(
        "The model was implemented using a discrete-step integration (dt=1 day) to allow for daily "
        "control decisions. We evaluated three scenarios:\n"
        "1. Baseline: No vaccination interventions.\n"
        "2. Mortality Strategy: Priority given to Group 2 (Elderly) -> Group 1 -> Group 0.\n"
        "3. Transmission Strategy: Priority given to Group 0 (Young/Spreaders) -> Group 1 -> Group 2.\n\n"
        "Vaccination capacity was fixed at Nu_max doses per day starting at t=50."
    )

    # --- 3. SIMULATION RESULTS ---
    pdf.chapter_title('3. Simulation Results')
    pdf.chapter_body(
        "The simulation was executed over a 200-day horizon. The key performance indicator (KPI) "
        "measured was the Cumulative Total Deaths at the end of the simulation."
    )

    # Creating the Results Table
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(200, 220, 255)
    
    # Table Header
    pdf.cell(60, 10, 'Scenario', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Total Deaths', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Lives Saved', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Reduction (%)', 1, 1, 'C', 1)

    # Table Data (Using your provided numbers)
    pdf.set_font('Arial', '', 11)
    
    # Row 1: No Vaccine
    pdf.cell(60, 10, 'No Vaccine', 1, 0, 'L')
    pdf.cell(40, 10, '21,426', 1, 0, 'C')
    pdf.cell(40, 10, '-', 1, 0, 'C')
    pdf.cell(40, 10, '-', 1, 1, 'C')

    # Row 2: Strategy Elderly
    pdf.set_font('Arial', 'B', 11) # Bold this row as winner
    pdf.cell(60, 10, 'Strategy: Elderly First', 1, 0, 'L')
    pdf.cell(40, 10, '13,809', 1, 0, 'C')
    pdf.cell(40, 10, '7,617', 1, 0, 'C')
    pdf.cell(40, 10, '35.5%', 1, 1, 'C')
    pdf.set_font('Arial', '', 11)

    # Row 3: Strategy Young
    pdf.cell(60, 10, 'Strategy: Young First', 1, 0, 'L')
    pdf.cell(40, 10, '14,614', 1, 0, 'C')
    pdf.cell(40, 10, '6,812', 1, 0, 'C')
    pdf.cell(40, 10, '31.8%', 1, 1, 'C')

    pdf.ln(10)

    # --- 4. DISCUSSION ---
    pdf.chapter_title('4. Discussion and Analysis')
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, '4.1 Strategy Comparison: Mortality vs. Transmission', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, 
        "The results demonstrate that prioritizing the most vulnerable group (Elderly) yielded the "
        "lowest mortality, saving 805 more lives than the transmission-blocking strategy. "
        "While the 'Young First' strategy likely reduced the total number of infections by targeting "
        "super-spreaders, the 'leakage' of the virus to the unvaccinated elderly population proved "
        "fatal due to their significantly higher mortality rate (Mu_elderly).\n\n"
        "The Mortality Strategy (13,809 deaths) effectively decoupled the infection curve from the death curve, "
        "ensuring that even if the virus circulated among the young, it did not result in severe outcomes."
    )
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, '4.2 Impact of NPIs', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, 
        "As observed in the auxiliary plots (Scenario D), vaccination alone is rate-limited by capacity constraints. "
        "Without Non-Pharmaceutical Interventions (NPIs), the epidemic peak occurs before the vaccination "
        "campaign reaches herd immunity thresholds. The optimal approach identified involves applying NPIs "
        "to delay the peak, buying time for the 'Elderly First' strategy to maximize coverage."
    )

    # --- 5. CONCLUSION ---
    pdf.ln(5)
    pdf.chapter_title('5. Conclusion')
    pdf.chapter_body(
        "The Multi-Group SIQRS model successfully highlights the trade-offs in vaccination policies. "
        "Under the simulated parameters, a direct protection strategy (Vaccinating the Vulnerable) "
        "proved to be 3.7% more effective in reducing mortality than a transmission-blocking strategy. "
        "We conclude that when vaccine supply is limited and fatality rates vary significantly by group, "
        "minimizing mortality requires prioritizing high-risk groups over high-contact groups."
    )

    pdf.output('Lab11_Final_Report.pdf')
    print("PDF Generated Successfully: Lab11_Final_Report.pdf")

if __name__ == '__main__':
    create_final_report()