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

.center-button {
    text-align: center;
}

.driver-labels {
    font-weight: bold;
    color: #2C3E50;
}

/* Toggle Switch Styling */
.toggle-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 15px 0;
}

.toggle-title {
    font-weight: bold;
    margin-bottom: 10px;
    font-size: 16px;
    color: #2C3E50;
}

.switch-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.switch-label {
    font-weight: bold;
    font-size: 18px;
    color: #7f8c8d;
    padding: 0 15px;
}

.switch-label.active {
    color: #2C3E50;
}

.switch {
    position: relative;
    display: inline-block;
    width: 80px;
    height: 40px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 34px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 32px;
    width: 32px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: #9B59B6; /* Purple for Kendrick */
}

input:not(:checked) + .slider {
    background-color: #3498DB; /* Blue for Drake */
}

input:focus + .slider {
    box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
    transform: translateX(40px);
}

/* Rounded sliders */
.slider.round {
    border-radius: 34px;
}

.slider.round:before {
    border-radius: 50%;
}

/* Make Drake blue and Kendrick purple */
.drake-label {
    color: #3498DB;
}

.kendrick-label {
    color: #9B59B6;
}

.drake-label.active {
    font-weight: bold;
    text-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

.kendrick-label.active {
    font-weight: bold;
    text-shadow: 0 0 5px rgba(155, 89, 182, 0.5);
}
"""


# Custom toggle switch HTML
def driver_toggle_switch():
    # Create a custom toggle switch HTML
    return ui.div(
        {"class": "toggle-container"},
        ui.div({"class": "toggle-title"}, "Select Good Driver:"),
        ui.div(
            {"class": "switch-container"},
            ui.div({"class": "switch-label drake-label", "id": "drake-label"}, "Drake"),
            ui.div(
                {"class": "switch"},
                ui.tags.input({"type": "checkbox", "id": "selected_good_driver", "name": "selected_good_driver",
                               "value": "kendrick"}),
                ui.tags.span({"class": "slider round"})
            ),
            ui.div({"class": "switch-label kendrick-label", "id": "kendrick-label"}, "Kendrick")
        ),
        # Add JavaScript to handle the toggle and label styling
        ui.tags.script("""
        $(document).ready(function() {
            // Set initial state
            updateLabels();

            // Update labels when switch changes
            $("#selected_good_driver").change(function() {
                updateLabels();
            });

            function updateLabels() {
                if($("#selected_good_driver").is(":checked")) {
                    // Kendrick is selected
                    $("#drake-label").removeClass("active");
                    $("#kendrick-label").addClass("active");
                } else {
                    // Drake is selected
                    $("#drake-label").addClass("active");
                    $("#kendrick-label").removeClass("active");
                }
            }
        });
        """)
    )


# App UI - improved layout with toggle switch for driver selection
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
                     # Driver selection toggle switch
                     ui.row(
                         ui.column(12, driver_toggle_switch())
                     ),
                     # Sliders row - with dynamic labels
                     ui.row(
                         ui.column(3,
                                   ui.input_slider("base_frequency", "Accident Frequency (Good Driver):",
                                                   min=0.01, max=0.10, value=0.03, step=0.01)
                                   ),
                         ui.column(3,
                                   ui.input_slider("base_severity", "Claim Amount (Good Driver):",
                                                   min=2000, max=10000, value=5000, step=500)
                                   ),
                         ui.column(3,
                                   ui.div({"class": "driver-labels"},
                                          ui.output_text("bad_driver_freq_label")),
                                   ui.input_slider("freq_multiplier", "",
                                                   min=1.5, max=5.0, value=3.0, step=0.5)
                                   ),
                         ui.column(3,
                                   ui.div({"class": "driver-labels"},
                                          ui.output_text("bad_driver_severity_label")),
                                   ui.input_slider("severity_multiplier", "",
                                                   min=1.2, max=3.0, value=2.0, step=0.2)
                                   )
                     ),
                     # CENTERED Re-simulate button
                     ui.row(
                         ui.column(5),  # Spacing
                         ui.column(2,
                                   ui.br(),
                                   ui.div({"class": "center-button"},
                                          ui.input_action_button("resim_drivers", "Re-simulate", class_="btn-resim")
                                          )
                                   ),
                         ui.column(5)  # Spacing
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "seed-info", "style": "text-align: center;"},
                                          ui.output_text("driver_seed_info")
                                          )
                                   )
                     ),
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
                     # Output text row showing we're using values from previous tab
                     ui.row(
                         ui.column(12,
                                   ui.div({"style": "text-align: center; margin-bottom: 20px;"},
                                          "Using values from Driver Comparison tab"
                                          )
                                   )
                     ),
                     # Information about the inherited values
                     ui.row(
                         ui.column(3,
                                   ui.div({"style": "text-align: center;"},
                                          ui.strong("Good Driver:"),
                                          ui.br(),
                                          ui.output_text("premium_good_driver_info")
                                          )
                                   ),
                         ui.column(3,
                                   ui.div({"style": "text-align: center;"},
                                          ui.strong("Good Driver Frequency:"),
                                          ui.br(),
                                          ui.output_text("premium_good_freq_info")
                                          )
                                   ),
                         ui.column(3,
                                   ui.div({"style": "text-align: center;"},
                                          ui.strong("Good Driver Severity:"),
                                          ui.br(),
                                          ui.output_text("premium_good_severity_info")
                                          )
                                   ),
                         ui.column(3,
                                   ui.div({"style": "text-align: center;"},
                                          ui.output_text("premium_bad_driver_label"),
                                          ui.br(),
                                          ui.output_text("premium_bad_info")
                                          )
                                   )
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

    # Helper function to get the selected good driver
    @reactive.Calc
    def get_good_driver():
        # Check if the checkbox is checked (true = kendrick, false = drake)
        return "kendrick" if input.selected_good_driver() else "drake"

    # Helper function to get the bad driver name
    def get_bad_driver_name():
        good_driver = get_good_driver()
        return "Kendrick" if good_driver == "drake" else "Drake"

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

    # Dynamic labels for bad driver
    @output
    @render.text
    def bad_driver_freq_label():
        bad_driver = get_bad_driver_name()
        return f"{bad_driver} Driving Frequency Multiplier:"

    @output
    @render.text
    def bad_driver_severity_label():
        bad_driver = get_bad_driver_name()
        return f"{bad_driver} Claim Amount Multiplier:"

    @output
    @render.text
    def premium_bad_driver_label():
        return f"<strong>{get_bad_driver_name()} Values:</strong>"

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
        text += f"• With Insurance: Everyone pays a premium of ${stats['fair_premium']:,.0f}.\n"
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
        good_driver = get_good_driver()
        good_driver_image = f"{good_driver}.jpeg"
        print(f"Driver Comparison using seed: {seed} (base: {base}, offset: {offset}, good driver: {good_driver})")
        return demonstrate_driver_comparison(
            input.base_frequency(),
            input.base_severity(),
            input.freq_multiplier(),
            input.severity_multiplier(),
            seed=seed,
            return_fig=True,
            good_driver_image=good_driver_image
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
        good_driver = get_good_driver().capitalize()
        bad_driver = get_bad_driver_name()

        text = "Risk Profile Interpretation:\n"
        text += f"• {good_driver} (Good Driver) has an average accident frequency of {stats['good_avg_frequency']:.1%} and an average claim amount of ${stats['good_avg_severity']:,.0f}\n"
        text += f"• {bad_driver} (Bad Driver) has an average accident frequency of {stats['bad_avg_frequency']:.1%} and an average claim amount of ${stats['bad_avg_severity']:,.0f}\n\n"

        text += f"• Frequency Difference: {bad_driver} has {stats['freq_multiplier']:.1f}x more frequent accidents than {good_driver}\n"
        text += f"• Claim Amount Difference: {bad_driver}'s claims are {stats['severity_multiplier']:.1f}x more costly than {good_driver}'s claims\n\n"

        text += f"• Expected Annual Cost - {good_driver}: ${stats['good_avg_frequency'] * stats['good_avg_severity']:,.0f} per driver\n"
        text += f"• Expected Annual Cost - {bad_driver}: ${stats['bad_avg_frequency'] * stats['bad_avg_severity']:,.0f} per driver\n"
        text += f"• Overall Risk Difference: {bad_driver} generates {stats['loss_multiplier']:.1f}x more in expected losses\n\n"

        text += "• Key Insight: The scatterplot illustrates why insurance companies segment drivers into risk groups.\n"
        text += "  Both frequency and claim amounts contribute to the overall cost differences between driver groups.\n"
        text += "  Each dot represents an individual driver's risk profile, showing natural variation within groups."

        return text

    # Display premium calculation tab info about inherited values
    @output
    @render.text
    def premium_good_driver_info():
        return f"{get_good_driver().capitalize()}"

    @output
    @render.text
    def premium_good_freq_info():
        _, stats = driver_data()
        return f"{stats['good_avg_frequency']:.1%}"

    @output
    @render.text
    def premium_good_severity_info():
        _, stats = driver_data()
        return f"${stats['good_avg_severity']:,.0f}"

    @output
    @render.text
    def premium_bad_info():
        _, stats = driver_data()
        return f"Freq: {stats['bad_avg_frequency']:.1%}, Severity: ${stats['bad_avg_severity']:,.0f}"

    # Premium Calculation Module - Now uses values from driver comparison
    @reactive.Calc
    def premium_calc_data():
        # Get driver data from previous tab
        _, driver_stats = driver_data()

        # Use the good and bad driver data from driver comparison
        good_freq = driver_stats['good_avg_frequency']
        good_severity = driver_stats['good_avg_severity']
        bad_freq = driver_stats['bad_avg_frequency']
        bad_severity = driver_stats['bad_avg_severity']
        good_driver = get_good_driver()
        good_driver_image = f"{good_driver}.jpeg"

        # Pass values to premium calculation
        return demonstrate_premium_calculation(
            accident_frequency=good_freq,
            claim_severity=good_severity,
            bad_driver_freq=bad_freq,
            bad_driver_severity=bad_severity,
            good_driver_image=good_driver_image,
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
        _, driver_stats = driver_data()

        good_freq = driver_stats['good_avg_frequency']
        good_severity = driver_stats['good_avg_severity']
        bad_freq = driver_stats['bad_avg_frequency']
        bad_severity = driver_stats['bad_avg_severity']
        good_driver = get_good_driver().capitalize()
        bad_driver = get_bad_driver_name()

        expense_ratio = 0.25
        risk_margin_ratio = 0.05

        text = "Insurance Premium Comparison:\n"
        text += f"• {good_driver} (Good Driver):\n"
        text += f"  - Accident Frequency: {good_freq:.1%} (probability of claim per year)\n"
        text += f"  - Average Claim Severity: ${good_severity:,.0f} (average cost when a claim occurs)\n"
        text += f"  - Expected Loss: ${stats['expected_loss']:,.2f} (frequency × severity)\n"
        text += f"  - Expenses: ${stats['expenses']:,.2f} ({expense_ratio:.0%} of premium)\n"
        text += f"  - Risk Margin: ${stats['risk_margin']:,.2f} ({risk_margin_ratio:.0%} of premium)\n"
        text += f"  - Final Premium: ${stats['premium']:,.2f}\n\n"

        text += f"• {bad_driver} (Bad Driver):\n"
        text += f"  - Accident Frequency: {bad_freq:.1%} (probability of claim per year)\n"
        text += f"  - Average Claim Severity: ${bad_severity:,.0f} (average cost when a claim occurs)\n"
        text += f"  - Expected Loss: ${stats['expected_loss_bad']:,.2f} (frequency × severity)\n"
        text += f"  - Expenses: ${stats['expenses_bad']:,.2f} ({expense_ratio:.0%} of premium)\n"
        text += f"  - Risk Margin: ${stats['risk_margin_bad']:,.2f} ({risk_margin_ratio:.0%} of premium)\n"
        text += f"  - Final Premium: ${stats['premium_bad']:,.2f}\n\n"

        premium_diff = stats['premium_bad'] - stats['premium']
        premium_ratio = stats['premium_bad'] / stats['premium']

        text += f"• Premium Difference: ${premium_diff:,.2f} ({premium_ratio:.1f}x higher for {bad_driver})\n\n"

        text += "• Key Insights:\n"
        text += f"  1. The premium calculation formula is: Premium = Expected Loss / (1 - Expense Ratio - Risk Margin)\n"
        text += f"  2. Both frequency and severity directly affect the premium - if either doubles, expected loss doubles\n"
        text += f"  3. A driver with {premium_ratio:.1f}x higher risk pays {premium_ratio:.1f}x higher premium\n"
        text += f"  4. The expense and risk margin components are proportionally larger for higher-risk drivers\n"

        return text


# Create and run the app
app = App(app_ui, server)