from shiny import App, ui, render, reactive
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
import random
import time

# Import the demonstration modules
from modules.risk_pooling import demonstrate_risk_pooling
from modules.driver_comparison import demonstrate_driver_comparison
from modules.premium_calculation import demonstrate_premium_calculation

# Define CSS for better styling
custom_css = """
.title-box {
    text-align: center;
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 15px;
}

.module-description {
    text-align: center;
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 0;
    color: #2C3E50;
}

.plot-title {
    text-align: center;
    font-weight: bold;
    font-size: 20px;
    margin-bottom: 15px;
    color: #2C3E50;
}

.plot-container {
    margin-bottom: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    padding: 15px;
    background-color: #ffffff;
}

.interpretation-box {
    margin-top: 20px;
    background-color: #E8F4FD;
    border-radius: 5px;
    padding: 15px;
    border-left: 5px solid #3498DB;
}

.interpretation-box pre {
    font-family: inherit;
    white-space: pre-wrap;
    margin: 0;
    font-size: 14px;
    line-height: 1.4;
}

.btn-resim {
    background-color: #3498DB;
    border-color: #2980B9;
    color: white;
    font-weight: bold;
    width: 100%;
}

.btn-resim:hover {
    background-color: #2980B9;
}

.seed-info {
    font-style: italic;
    font-size: 12px;
    color: #666;
    margin-top: 5px;
}
"""

# App UI - improved layout with re-simulate buttons
app_ui = ui.page_fluid(
    ui.tags.style(custom_css),
    ui.h1("Insurance Fundamentals", style="text-align: center; margin-bottom: 10px;"),
    ui.p("Interactive demonstrations of key insurance concepts", style="text-align: center; margin-bottom: 20px;"),

    ui.navset_tab(
        # 1. RISK POOLING MODULE
        ui.nav_panel("1. Risk Pooling",
                     # Title in its own row
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "Risk pooling shows how insurance distributes risk across many policyholders."
                                                 )
                                          )
                                   )
                     ),
                     # Sliders and button in the next row
                     ui.row(
                         ui.column(3,
                                   ui.input_slider("accident_probability", "Accident Probability:",
                                                   min=0.01, max=0.25, value=0.05, step=0.01)
                                   ),
                         ui.column(3,
                                   ui.input_slider("num_policyholders", "Number of Policyholders:",
                                                   min=10, max=1000, value=100, step=10)
                                   ),
                         ui.column(2,
                                   ui.br(),
                                   ui.input_action_button("resim_risk", "Re-simulate", class_="btn-resim")
                                   ),
                         ui.column(4,
                                   ui.br(),
                                   ui.div({"class": "seed-info"}, ui.output_text("risk_seed_info"))
                                   )
                     ),
                     ui.hr(),
                     # Main content below with clear separation
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Individual vs Pooled Risk"),
                            ui.output_plot("risk_pooling_plot", width="100%", height="500px")
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("risk_pooling_interpretation"))
                            )
                     ),

        # 2. DRIVER COMPARISON MODULE
        ui.nav_panel("2. Driver Comparison",
                     # Title in its own row
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "Visualize how frequency and severity create distinct risk clusters for different driver types."
                                                 )
                                          )
                                   )
                     ),
                     # Sliders and button in the next row
                     ui.row(
                         ui.column(2),  # Add empty column for spacing (making sliders narrower)
                         ui.column(2,
                                   ui.input_slider("base_frequency", "Accident Frequency (Good Drivers):",
                                                   min=0.01, max=0.10, value=0.03, step=0.01)
                                   ),
                         ui.column(2,
                                   ui.input_slider("base_severity", "Claim Amount (Good Drivers):",
                                                   min=2000, max=10000, value=5000, step=500)
                                   ),
                         ui.column(2,
                                   ui.input_slider("freq_multiplier", "Bad Driver Frequency Multiplier:",
                                                   min=1.5, max=5.0, value=3.0, step=0.5)
                                   ),
                         ui.column(2,
                                   ui.input_slider("severity_multiplier", "Bad Driver Claim Amount Multiplier:",
                                                   min=1.2, max=3.0, value=2.0, step=0.2)
                                   ),
                         ui.column(2),  # Add empty column for spacing
                     ),
                     ui.row(
                         ui.column(10),  # Spacing
                         ui.column(2,
                                   ui.br(),
                                   ui.input_action_button("resim_drivers", "Re-simulate", class_="btn-resim"),
                                   ui.br(),
                                   ui.div({"class": "seed-info"}, ui.output_text("driver_seed_info"))
                                   )
                     ),
                     # Remove this row since we moved the seed info
                     # ui.row(
                     #     ui.column(12,
                     #               ui.br(),
                     #               ui.div({"class": "seed-info"}, ui.output_text("driver_seed_info"))
                     #               )
                     # ),
                     ui.hr(),
                     # Main content below with clear separation
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Driver Risk Profiles: Frequency vs Claim Amount"),
                            ui.output_plot("driver_comparison_plot", width="100%", height="700px")
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("driver_comparison_interpretation"))
                            )
                     ),

        # 3. PREMIUM CALCULATION MODULE
        ui.nav_panel("3. Premium Calculation",
                     # Title in its own row
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "Demonstrates how insurance premiums are calculated based on frequency, severity, and other factors."
                                                 )
                                          )
                                   )
                     ),
                     # Sliders row - NO re-simulate button for this deterministic module
                     ui.row(
                         ui.column(4,
                                   ui.input_slider("accident_frequency", "Accident Frequency:",
                                                   min=0.01, max=0.20, value=0.05, step=0.01)
                                   ),
                         ui.column(4,
                                   ui.input_slider("claim_severity", "Claim Severity ($):",
                                                   min=2000, max=20000, value=8000, step=1000)
                                   ),
                         ui.column(4)
                     ),
                     ui.hr(),
                     # Main content below with clear separation
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Premium Components and Breakdown"),
                            ui.output_plot("premium_calc_plot", width="100%", height="600px")
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("premium_calc_interpretation"))
                            )
                     )
    )
)


# Server logic
def server(input, output, session):
    # Reactive values to track simulation offsets
    risk_sim_offset = reactive.Value(0)
    driver_sim_offset = reactive.Value(0)

    # Update offset values when re-simulate buttons are clicked
    @reactive.Effect
    @reactive.event(input.resim_risk)
    def _update_risk_seed():
        new_offset = random.randint(1, 10000)
        risk_sim_offset.set(new_offset)
        print(f"Risk pooling seed offset updated to: {new_offset}")

    @reactive.Effect
    @reactive.event(input.resim_drivers)
    def _update_driver_seed():
        new_offset = random.randint(1, 10000)
        driver_sim_offset.set(new_offset)
        print(f"Driver comparison seed offset updated to: {new_offset}")

    # Reactive calculations for seed values
    @reactive.Calc
    def risk_seed():
        base_seed = int(input.accident_probability() * 10000 + input.num_policyholders())
        offset = risk_sim_offset.get()
        return base_seed + offset, base_seed, offset

    @reactive.Calc
    def driver_seed():
        base_seed = int(input.base_frequency() * 10000 + input.base_severity() +
                        input.freq_multiplier() * 100 + input.severity_multiplier() * 100)
        offset = driver_sim_offset.get()
        return base_seed + offset, base_seed, offset

    # Display seed info in UI
    @output
    @render.text
    def risk_seed_info():
        seed, base, offset = risk_seed()
        return f"Seed: {seed} (Base: {base}, Offset: {offset})"

    @output
    @render.text
    def driver_seed_info():
        seed, base, offset = driver_seed()
        return f"Seed: {seed} (Base: {base}, Offset: {offset})"

    # Risk Pooling Module
    @reactive.Calc
    def risk_data():
        seed, base, offset = risk_seed()
        print(f"Risk Pooling using seed: {seed} (base: {base}, offset: {offset})")
        return demonstrate_risk_pooling(
            input.accident_probability(),
            input.num_policyholders(),
            seed=seed,
            return_fig=True
        )

    @output
    @render.plot
    def risk_pooling_plot():
        fig, _ = risk_data()
        return fig

    @output
    @render.text
    def risk_pooling_interpretation():
        _, stats = risk_data()
        claim_amount = 20000  # Fixed claim amount

        text = "Insurance Interpretation:\n"
        text += f"• Individual Risk: Each person has a {input.accident_probability():.1%} chance of a ${claim_amount:,.0f} loss.\n"
        text += f"• Without Insurance: {stats['num_with_loss']} people ({stats['percent_with_loss']:.1f}%) faced a ${claim_amount:,.0f} loss in this simulation.\n"
        text += f"• With Insurance: Everyone pays a premium of ${stats['fair_premium']:.0f}.\n"
        text += f"• Risk Pooling Result: The insurer collected ${stats['pool_premium_total']:,.0f} and paid ${stats['total_losses']:,.0f} in claims.\n"

        if stats['pool_performance'] < 1:
            text += f"• This year the insurance pool had a ${abs(stats['pool_premium_total'] - stats['total_losses']):,.0f} surplus.\n"
            text += "• The surplus can be held as capital to handle future years when claims exceed premiums.\n"
        else:
            text += f"• This year the insurance pool had a ${abs(stats['pool_premium_total'] - stats['total_losses']):,.0f} deficit.\n"
            text += "• The deficit must be covered by the insurer's capital reserves.\n"

        text += f"• Key Insight: As the number of policyholders increases, the 'Actual/Expected' ratio approaches 1.0, "
        text += f"making the insurance pool's results more predictable and stable."

        return text

    # Driver Comparison Module
    @reactive.Calc
    def driver_data():
        seed, base, offset = driver_seed()
        print(f"Driver Comparison using seed: {seed} (base: {base}, offset: {offset})")
        return demonstrate_driver_comparison(
            input.base_frequency(),
            input.base_severity(),
            input.freq_multiplier(),
            input.severity_multiplier(),
            seed=seed,
            return_fig=True
        )

    @output
    @render.plot
    def driver_comparison_plot():
        fig, _ = driver_data()
        return fig

    @output
    @render.text
    def driver_comparison_interpretation():
        _, stats = driver_data()

        text = "Risk Profile Interpretation:\n"
        text += f"• Good Drivers have an average accident frequency of {stats['good_avg_frequency']:.1%} and an average claim amount of ${stats['good_avg_severity']:.0f}\n"
        text += f"• Bad Drivers have an average accident frequency of {stats['bad_avg_frequency']:.1%} and an average claim amount of ${stats['bad_avg_severity']:.0f}\n\n"

        text += f"• Frequency Difference: Bad drivers have {stats['freq_multiplier']:.1f}x more frequent accidents than good drivers\n"
        text += f"• Claim Amount Difference: Bad driver claims are {stats['severity_multiplier']:.1f}x more costly than good driver claims\n\n"

        text += f"• Expected Annual Cost - Good Drivers: ${stats['good_avg_frequency'] * stats['good_avg_severity']:.0f} per driver\n"
        text += f"• Expected Annual Cost - Bad Drivers: ${stats['bad_avg_frequency'] * stats['bad_avg_severity']:.0f} per driver\n"
        text += f"• Overall Risk Difference: Bad drivers generate {stats['loss_multiplier']:.1f}x more in expected losses\n\n"

        text += "• Key Insight: The scatterplot illustrates why insurance companies segment drivers into risk groups.\n"
        text += "  Both frequency and claim amounts contribute to the overall cost differences between driver groups.\n"
        text += "  Each dot represents an individual driver's risk profile, showing natural variation within groups."

        return text

    # Premium Calculation Module
    @reactive.Calc
    def premium_calc_data():
        # Simply pass the parameters directly - no randomness
        return demonstrate_premium_calculation(
            input.accident_frequency(),
            input.claim_severity(),
            return_fig=True
        )

    @output
    @render.plot
    def premium_calc_plot():
        fig, _ = premium_calc_data()
        return fig

    @output
    @render.text
    def premium_calc_interpretation():
        _, stats = premium_calc_data()

        expense_ratio = 0.25
        risk_margin_ratio = 0.05

        text = "Insurance Interpretation:\n"
        text += f"• Accident Frequency: {input.accident_frequency():.1%} (probability of claim per year)\n"
        text += f"• Average Claim Severity: ${input.claim_severity():,.0f} (average cost when a claim occurs)\n"
        text += f"• Expected Loss: ${stats['expected_loss']:.2f} (pure cost of risk)\n"
        text += f"• Expenses: ${stats['expenses']:.2f} ({expense_ratio:.0%} of premium for administration, commissions, etc.)\n"
        text += f"• Risk Margin: ${stats['risk_margin']:.2f} ({risk_margin_ratio:.0%} of premium for profit and uncertainty)\n"
        text += f"• Final Premium: ${stats['premium']:.2f}\n"
        text += "• This is the base premium before applying individual rating factors like age, driving history, etc."

        return text


# Create and run the app
app = App(app_ui, server)