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

/* Add extra bottom padding for plot container to fix cut-off label */
.plot-container-extra-bottom {
    padding-bottom: 50px !important;
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
    cursor: pointer;
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

/* Highlight for premium difference */
.premium-diff-highlight {
    background: linear-gradient(to right, #3498DB, #9B59B6);
    color: white;
    padding: 8px 15px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    font-weight: bold;
    text-align: center;
    margin: 10px auto;
    max-width: 80%;
}

/* Highlight for "Using values from" text */
.values-from-highlight {
    background-color: #3498DB;
    color: white;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
    margin: 10px auto 20px auto;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    width: 80%;
    max-width: 600px;
}

/* Value display text */
.value-display {
    font-weight: bold;
    color: #2C3E50;
    font-size: 16px;
}

/* Ethics tab styling */
.ethics-container {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.ethics-intro {
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.ethics-question {
    background-color: #E8F4FD;
    border-left: 5px solid #3498DB;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 5px;
    transition: all 0.3s ease;
}

.ethics-question p {
    white-space: normal;  /* Fix for wrapping issues */
    word-wrap: break-word;
    margin-bottom: 10px;
}

.ethics-question-title {
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 10px;
    color: #2C3E50;
}

.ethical-variable {
    background-color: rgba(46, 204, 113, 0.2);
    border-left: 5px solid #2ECC71;
}

.unethical-variable {
    background-color: rgba(231, 76, 60, 0.2);
    border-left: 5px solid #E74C3C;
}

.ethics-grade {
    background-color: #E8F8F5;
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
    border: 1px solid #2ECC71;
    text-align: center;
}

.ethics-grade h3 {
    margin-top: 0;
    color: #2C3E50;
}

.ethics-grade span {
    font-size: 24px;
    font-weight: bold;
    color: #2ECC71;
}

.ethics-feedback {
    margin-top: 10px;
    font-style: italic;
}

.grade-btn {
    background-color: #2ECC71;
    border-color: #27AE60;
    color: white;
    font-weight: bold;
    margin-top: 15px;
}

.grade-btn:hover {
    background-color: #27AE60;
}
"""


# Custom toggle switch HTML
def driver_toggle_switch():
    # Create a custom toggle switch HTML
    return ui.div(
        {"class": "toggle-container"},
        ui.div({"class": "toggle-title"}, "Select Low Risk Driver:"),
        ui.div(
            {"class": "switch-container"},
            ui.div({"class": "switch-label drake-label active", "id": "drake-label",
                    "onclick": "document.getElementById('toggle_driver').checked = false; $(document).trigger('shiny:inputchanged'); updateLabels();"},
                   "Drake"),
            ui.div(
                {"class": "switch"},
                ui.tags.input(
                    {"type": "checkbox", "id": "toggle_driver", "name": "selected_good_driver", "value": "kendrick",
                     "onchange": "updateLabels();"}),
                ui.tags.label({"for": "toggle_driver", "class": "slider round"})
            ),
            ui.div({"class": "switch-label kendrick-label", "id": "kendrick-label",
                    "onclick": "document.getElementById('toggle_driver').checked = true; $(document).trigger('shiny:inputchanged'); updateLabels();"},
                   "Kendrick")
        ),
        # Add JavaScript to handle the toggle and label styling
        ui.tags.script("""
        function updateLabels() {
            if($("#toggle_driver").is(":checked")) {
                // Kendrick is selected
                $("#drake-label").removeClass("active");
                $("#kendrick-label").addClass("active");
                Shiny.setInputValue("selected_good_driver", "kendrick");
            } else {
                // Drake is selected
                $("#drake-label").addClass("active");
                $("#kendrick-label").removeClass("active");
                Shiny.setInputValue("selected_good_driver", "drake");
            }
        }

        $(document).ready(function() {
            // Set initial state
            updateLabels();

            // Make sure slider click works
            $(".slider").click(function(e) {
                // Don't let event bubble up to prevent double-toggling
                e.stopPropagation();
            });
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
                     # Sliders row - with dynamic labels (shortened "Estimated" to "Est.")
                     ui.row(
                         ui.column(3,
                                   ui.input_slider("base_frequency", "Est. Accident Frequency (Low Risk):",
                                                   min=0.01, max=0.10, value=0.03, step=0.01)
                                   ),
                         ui.column(3,
                                   ui.input_slider("base_severity", "Est. Claim Amount (Low Risk):",
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
                     # Main content below with clear separation - ADDED EXTRA BOTTOM PADDING
                     ui.div({"class": "plot-container plot-container-extra-bottom"},
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
                     # Output text row showing we're using values from previous tab - HIGHLIGHTED
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "values-from-highlight"},
                                          "Using values from Driver Comparison tab"
                                          )
                                   )
                     ),
                     # Information about the inherited values
                     ui.row(
                         ui.column(3,
                                   ui.div({"style": "text-align: center;"},
                                          ui.output_ui("premium_first_cohort_label"),
                                          ui.br(),
                                          ui.div({"class": "value-display"},
                                                 ui.output_text("premium_good_driver_info"))
                                          )
                                   ),
                         ui.column(3,
                                   ui.div({"style": "text-align: center;"},
                                          ui.strong("Est. Frequency:"),
                                          ui.br(),
                                          ui.div({"class": "value-display"},
                                                 ui.output_text("premium_good_freq_info"))
                                          )
                                   ),
                         ui.column(3,
                                   ui.div({"style": "text-align: center;"},
                                          ui.strong("Est. Severity:"),
                                          ui.br(),
                                          ui.div({"class": "value-display"},
                                                 ui.output_text("premium_good_severity_info"))
                                          )
                                   ),
                         ui.column(3,
                                   ui.div({"style": "text-align: center;"},
                                          # Using output_ui for HTML content
                                          ui.output_ui("premium_bad_driver_label"),
                                          ui.br(),
                                          ui.div({"class": "value-display"},
                                                 ui.output_text("premium_bad_info"))
                                          )
                                   )
                     ),
                     ui.hr(),
                     # Main content below with clear separation - INCREASED HEIGHT BY 100%
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Premium Components and Breakdown"),
                            ui.output_plot("premium_calc_plot", width="100%", height="1200px")
                            # Doubled from 600px to 1200px
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("premium_calc_interpretation"))
                            )
                     ),

        # 4. ETHICS OF RATING MODULE - Updated to replace gender with religion
        ui.nav_panel("4. Ethics of Rating",
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "Explore the ethical considerations of using different rating variables in insurance."
                                                 )
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-container"},
                                          ui.div({"class": "ethics-intro"},
                                                 """
                                                 Insurance pricing relies on risk factors that predict future claims. However, not all potential 
                                                 rating variables are considered acceptable for use in setting premiums. The appropriate use of 
                                                 rating variables involves balancing actuarial concerns (like statistical predictive power) 
                                                 with social considerations (like fairness and potential discrimination).
   
                                                 Below are several potential rating variables. For each one, indicate whether you believe 
                                                 it would be appropriate to use in setting auto insurance rates.
                                                 """
                                                 )
                                          )
                                   )
                     ),
                     # Rating Variables to Evaluate - with ids for color coding
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "drake_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Drake Listeners"),
                                          ui.p("""Would it be ethical to charge different auto insurance rates based on whether 
                                          someone primarily listens to Drake's music?"""),
                                          ui.input_checkbox("drake_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "kendrick_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Kendrick Listeners"),
                                          ui.p("""Would it be ethical to charge different auto insurance rates based on whether 
                                          someone primarily listens to Kendrick Lamar's music?"""),
                                          ui.input_checkbox("kendrick_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "age_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Driver Age"),
                                          ui.p(
                                              """Would it be ethical to charge different auto insurance rates based on a driver's age?"""),
                                          ui.input_checkbox("age_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "vehicle_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Vehicle Type"),
                                          ui.p("""Would it be ethical to charge different auto insurance rates based on the type 
                                          of vehicle a person drives (sports car, sedan, SUV, etc.)?"""),
                                          ui.input_checkbox("vehicle_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "religion_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Religion"),
                                          ui.p(
                                              """Would it be ethical to charge different auto insurance rates based on a person's religion?"""),
                                          ui.input_checkbox("religion_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "race_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Race/Ethnicity"),
                                          ui.p("""Would it be ethical to charge different auto insurance rates based on a person's 
                                          race or ethnicity?"""),
                                          ui.input_checkbox("race_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "experience_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Years of Driving Experience"),
                                          ui.p("""Would it be ethical to charge different auto insurance rates based on how many 
                                          years a person has been driving?"""),
                                          ui.input_checkbox("experience_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "multiproduct_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Multi-Product Discount"),
                                          ui.p("""Would it be ethical to offer discounted auto insurance rates to customers who 
                                          also purchase other insurance products from the same company?"""),
                                          ui.input_checkbox("multiproduct_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "speeding_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Speeding Convictions"),
                                          ui.p("""Would it be ethical to charge different auto insurance rates based on a person's 
                                          history of speeding tickets and convictions?"""),
                                          ui.input_checkbox("speeding_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "driving_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Driving History"),
                                          ui.p("""Would it be ethical to charge different auto insurance rates based on a person's 
                                          past driving record (accidents, tickets, etc.)?"""),
                                          ui.input_checkbox("driving_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     # Grade Button
                     ui.row(
                         ui.column(4),  # For spacing
                         ui.column(4,
                                   ui.div({"class": "center-button"},
                                          ui.input_action_button("grade_ethics", "Grade My Answers",
                                                                 class_="btn-resim grade-btn")
                                          )
                                   ),
                         ui.column(4)  # For spacing
                     ),
                     # Grade Results (initially hidden)
                     ui.row(
                         ui.column(12, ui.output_ui("ethics_grade_output"))
                     ),
                     # Add JavaScript for color coding - updated to replace gender with religion
                     ui.tags.script("""
                    $(document).ready(function() {
                        $('#grade_ethics').click(function() {
                            // Wait a moment for the grade to be calculated
                            setTimeout(function() {
                                // Remove any existing coloring
                                $('.ethics-question').removeClass('ethical-variable unethical-variable');

                                // Color the blocks based on correct answers
                                $('#drake_rating_block').addClass('unethical-variable');
                                $('#kendrick_rating_block').addClass('unethical-variable');
                                $('#age_rating_block').addClass('ethical-variable');
                                $('#vehicle_rating_block').addClass('ethical-variable');
                                $('#religion_rating_block').addClass('unethical-variable');
                                $('#race_rating_block').addClass('unethical-variable');
                                $('#experience_rating_block').addClass('ethical-variable');
                                $('#multiproduct_rating_block').addClass('ethical-variable');
                                $('#speeding_rating_block').addClass('ethical-variable');
                                $('#driving_rating_block').addClass('ethical-variable');
                            }, 500);
                        });
                    });
                    """)
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
        # Get the value from the selected_good_driver input
        return input.selected_good_driver()

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

    # Dynamic labels for second cohort
    @output
    @render.text
    def bad_driver_freq_label():
        bad_driver = get_bad_driver_name()
        return f"{bad_driver} Cohort Frequency Multiplier:"

    @output
    @render.text
    def bad_driver_severity_label():
        bad_driver = get_bad_driver_name()
        return f"{bad_driver} Cohort Claim Amount Multiplier:"

    # Using render.ui for HTML content - now with specific cohort names
    @output
    @render.ui
    def premium_bad_driver_label():
        bad_driver = get_bad_driver_name()
        return ui.strong(f"{bad_driver} Cohort:")

    @output
    @render.ui
    def premium_first_cohort_label():
        good_driver = get_good_driver().capitalize()
        return ui.strong(f"{good_driver} Cohort:")

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

        # Use specific cohort names
        first_cohort = f"{good_driver} Cohort"
        second_cohort = f"{bad_driver} Cohort"

        text = "Risk Profile Interpretation:\n"
        text += f"• {first_cohort} has an est. accident frequency of {stats['good_avg_frequency']:.1%} and an est. average claim amount of ${stats['good_avg_severity']:,.0f}\n"
        text += f"• {second_cohort} has an est. accident frequency of {stats['bad_avg_frequency']:.1%} and an est. average claim amount of ${stats['bad_avg_severity']:,.0f}\n\n"

        text += f"• Frequency Difference: {second_cohort} has {stats['freq_multiplier']:.1f}x more frequent accidents than {first_cohort}\n"
        text += f"• Claim Amount Difference: {second_cohort}'s claims are {stats['severity_multiplier']:.1f}x more costly than {first_cohort}'s claims\n\n"

        text += f"• Expected Annual Cost - {first_cohort}: ${stats['good_avg_frequency'] * stats['good_avg_severity']:,.0f} per driver\n"
        text += f"• Expected Annual Cost - {second_cohort}: ${stats['bad_avg_frequency'] * stats['bad_avg_severity']:,.0f} per driver\n"
        text += f"• Overall Risk Difference: {second_cohort} generates {stats['loss_multiplier']:.1f}x more in expected losses\n\n"

        text += "• Key Insight: The scatterplot illustrates why insurance companies segment drivers into risk cohorts.\n"
        text += "  Both frequency and claim amounts contribute to the overall cost differences between driver cohorts.\n"
        text += "  Each dot represents an individual driver's risk profile, showing natural variation within cohorts."

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

        # Use specific cohort names
        first_cohort = f"{good_driver} Cohort"
        second_cohort = f"{bad_driver} Cohort"

        expense_ratio = 0.25
        risk_margin_ratio = 0.05

        text = "Insurance Premium Comparison:\n"
        text += f"• {first_cohort}:\n"
        text += f"  - Est. Accident Frequency: {good_freq:.1%} (probability per year)\n"
        text += f"  - Est. Average Claim Severity: ${good_severity:,.0f} (average cost when a claim occurs)\n"
        text += f"  - Expected Loss: ${stats['expected_loss']:,.2f} (frequency × severity)\n"
        text += f"  - Expenses: ${stats['expenses']:,.2f} ({expense_ratio:.0%} of premium)\n"
        text += f"  - Risk Margin: ${stats['risk_margin']:,.2f} ({risk_margin_ratio:.0%} of premium)\n"
        text += f"  - Final Premium: ${stats['premium']:,.2f}\n\n"

        text += f"• {second_cohort}:\n"
        text += f"  - Est. Accident Frequency: {bad_freq:.1%} (probability per year)\n"
        text += f"  - Est. Average Claim Severity: ${bad_severity:,.0f} (average cost when a claim occurs)\n"
        text += f"  - Expected Loss: ${stats['expected_loss_bad']:,.2f} (frequency × severity)\n"
        text += f"  - Expenses: ${stats['expenses_bad']:,.2f} ({expense_ratio:.0%} of premium)\n"
        text += f"  - Risk Margin: ${stats['risk_margin_bad']:,.2f} ({risk_margin_ratio:.0%} of premium)\n"
        text += f"  - Final Premium: ${stats['premium_bad']:,.2f}\n\n"

        premium_diff = stats['premium_bad'] - stats['premium']
        premium_ratio = stats['premium_bad'] / stats['premium']

        text += f"• Premium Difference: ${premium_diff:,.2f} ({premium_ratio:.1f}x higher for {second_cohort})\n\n"

        text += "• Key Insights:\n"
        text += f"  1. The premium calculation formula is: Premium = Expected Loss / (1 - Expense Ratio - Risk Margin)\n"
        text += f"  2. Both frequency and severity directly affect the premium - if either doubles, expected loss doubles\n"
        text += f"  3. A driver cohort with {premium_ratio:.1f}x higher risk pays {premium_ratio:.1f}x higher premium\n"
        text += f"  4. The expense and risk margin components are proportionally larger for higher-risk driver cohorts\n"

        return text

    # Ethics Rating Module - Updated to replace gender with religion
    @reactive.Calc
    def calculate_ethics_grade():
        # These are the "model answers" based on general insurance standards
        model_answers = {
            'drake_rating': False,  # Not appropriate to use Drake listening as a rating factor
            'kendrick_rating': False,  # Not appropriate to use Kendrick listening as a rating factor
            'age_rating': True,  # Age is a commonly used rating factor
            'vehicle_rating': True,  # Vehicle type is a commonly used rating factor
            'religion_rating': False,  # Religion is not appropriate
            'race_rating': False,  # Race/ethnicity is not appropriate
            'experience_rating': True,  # Years of driving experience is a valid rating factor
            'multiproduct_rating': True,  # Multi-product discount is a common and accepted practice
            'speeding_rating': True,  # Speeding convictions are directly related to driving risk
            'driving_rating': True,  # Driving history is universally used
        }

        # Count correct answers
        correct = 0
        total = len(model_answers)

        # Track incorrect answers
        incorrect = []

        for var, model_answer in model_answers.items():
            user_answer = getattr(input, var)()
            if user_answer == model_answer:
                correct += 1
            else:
                # Format the variable name for displaying
                var_formatted = var.replace('_rating', '').replace('_', ' ').title()
                incorrect.append(var_formatted)

        # Calculate score out of 10
        score = round(correct / total * 10)

        # Generate feedback based on score
        if score >= 9:
            feedback = "Excellent! You have a strong understanding of ethical rating considerations."
        elif score >= 7:
            feedback = "Good work! You understand most of the key ethical rating principles."
        elif score >= 5:
            feedback = "You're on the right track. Consider how these variables relate to risk vs. potential discrimination."
        else:
            feedback = "Consider reviewing how insurers balance predictive value with social fairness."

        # Add specific feedback if there were incorrect answers
        if incorrect:
            feedback += f" You might want to reconsider your answers for: {', '.join(incorrect)}."

        return score, feedback, correct, total

    # Display ethics grade output
    @output
    @render.ui
    @reactive.event(input.grade_ethics)
    def ethics_grade_output():
        score, feedback, correct, total = calculate_ethics_grade()

        return ui.div(
            {"class": "ethics-grade"},
            ui.h3("Your Rating Variable Score:"),
            ui.span(f"{score}/10"),
            ui.p(f"You got {correct} out of {total} correct."),
            ui.div({"class": "ethics-feedback"}, feedback),
            ui.br(),
            ui.p("""
            Key considerations for rating variables include:
            • Actuarial justification (statistical correlation with risk)
            • Causality vs. correlation
            • Controllability (can a person change this factor?)
            • Social acceptability and potential for discrimination
            • Legality (some factors are prohibited by law in many jurisdictions)
            """),
            ui.HTML("""
        <p><b>Ethical rating variables</b> (shown in <span style="color: #2ECC71">green</span>) typically have direct causal 
        relationships with risk and are often within the driver's control. These include driving history, 
        speeding convictions, vehicle type, and years of experience.</p>
        """),
            ui.HTML("""
        <p><b>Unethical rating variables</b> (shown in <span style="color: #E74C3C">red</span>) are usually 
        discriminatory, outside a person's control, or lack direct causal links to driving behavior.
        These include race/ethnicity, religion, and music preferences.  Regulations prohibit their usage in rating.</p>
        """)
        )


# Create and run the app
app = App(app_ui, server)