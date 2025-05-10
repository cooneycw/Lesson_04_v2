import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.gridspec import GridSpec


def demonstrate_premium_calculation(accident_frequency=0.05, claim_severity=8000, return_fig=False,
                                    good_driver_image="drake.jpeg",
                                    bad_driver_freq=0.15, bad_driver_severity=16000):
    """
    Demonstrates how insurance premiums are calculated

    Parameters:
    -----------
    accident_frequency : float
        The probability of an accident
    claim_severity : float
        The average cost of a claim
    return_fig : bool
        If True, returns the figure and stats for Shiny integration
    good_driver_image : str
        Image file name for the good driver (drake.jpeg or kendrick.jpeg)
    bad_driver_freq : float
        Bad driver accident frequency (for comparison)
    bad_driver_severity : float
        Bad driver claim severity (for comparison)

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object (if return_fig is True)
    stats : dict
        Key statistics (if return_fig is True)
    """
    # Get driver names from the image filename
    good_driver_name = good_driver_image.split('.')[0].capitalize()
    bad_driver_name = "Kendrick" if good_driver_name == "Drake" else "Drake"

    # Use specific cohort names
    first_cohort_name = f"{good_driver_name} Cohort"
    second_cohort_name = f"{bad_driver_name} Cohort"

    # Calculate components for good driver
    expected_loss_good = accident_frequency * claim_severity
    expense_ratio = 0.25  # Fixed at 25% of premium
    risk_margin_ratio = 0.05  # Fixed at 5% of premium

    # Premium components (solving the equation)
    # Premium = Expected Loss + Expense Ratio × Premium + Risk Margin × Premium
    # Premium = Expected Loss / (1 - Expense Ratio - Risk Margin)
    premium_good = expected_loss_good / (1 - expense_ratio - risk_margin_ratio)
    expenses_good = premium_good * expense_ratio
    risk_margin_good = premium_good * risk_margin_ratio

    # Calculate components for bad driver
    expected_loss_bad = bad_driver_freq * bad_driver_severity
    premium_bad = expected_loss_bad / (1 - expense_ratio - risk_margin_ratio)
    expenses_bad = premium_bad * expense_ratio
    risk_margin_bad = premium_bad * risk_margin_ratio

    # Loading factor
    loading_factor_good = premium_good / expected_loss_good
    loading_factor_bad = premium_bad / expected_loss_bad

    # For Shiny integration
    if return_fig:
        # Create figure with more height to accommodate spacing and doubled height
        fig = Figure(figsize=(14, 28))  # Doubled height to make charts taller

        # Use GridSpec for better control of spacing
        gs = GridSpec(4, 2, height_ratios=[6, 1, 0.5, 6], hspace=0.5,
                      figure=fig)  # Doubled height_ratios[0] and height_ratios[3]

        # Top row: Bar charts
        ax1 = fig.add_subplot(gs[0, 0])  # Good driver bar chart
        ax2 = fig.add_subplot(gs[0, 1])  # Bad driver bar chart

        # Bottom row: Pie charts (with extra space between rows)
        ax3 = fig.add_subplot(gs[3, 0])  # Good driver pie chart
        ax4 = fig.add_subplot(gs[3, 1])  # Bad driver pie chart

        # Component lists
        components = ['Expected Loss', 'Expenses', 'Risk Margin']
        good_values = [expected_loss_good, expenses_good, risk_margin_good]
        bad_values = [expected_loss_bad, expenses_bad, risk_margin_bad]

        # Colors for both charts (consistent, improved colors)
        colors = ['#3498DB', '#2ECC71', '#9B59B6']  # Blue, Green, Purple

        # Determine the maximum value for both y-axes
        y_max = max(premium_bad * 1.2, premium_good * 1.2)

        # 1. GOOD DRIVER BAR CHART (TOP LEFT)
        bars1 = ax1.bar(components, good_values, color=colors, alpha=0.8, width=0.6)
        ax1.set_title(f'{first_cohort_name} Premium Components', fontsize=14)
        ax1.set_ylabel('Amount ($)', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)
        ax1.set_ylim(0, y_max)  # Same scale as other chart

        # Add premium line
        ax1.axhline(premium_good, color='#E74C3C', linestyle='--',
                    label=f'Premium: ${premium_good:,.2f}')
        ax1.legend(fontsize=10, loc='upper left')  # Move legend to avoid image

        # Add dollar value labels
        for bar, value in zip(bars1, good_values):
            percentage = value / premium_good * 100
            ax1.text(bar.get_x() + bar.get_width() / 2, value + (y_max * 0.02),
                     f'${value:,.0f}\n({percentage:.1f}%)',
                     ha='center', va='bottom',
                     fontsize=9)

        # Format y-axis with commas
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))

        # 2. BAD DRIVER BAR CHART (TOP RIGHT)
        bars2 = ax2.bar(components, bad_values, color=colors, alpha=0.8, width=0.6)
        ax2.set_title(f'{second_cohort_name} Premium Components', fontsize=14)
        ax2.set_ylabel('Amount ($)', fontsize=12)
        ax2.grid(axis='y', alpha=0.3)
        ax2.set_ylim(0, y_max)  # Same scale as other chart

        # Add premium line
        ax2.axhline(premium_bad, color='#E74C3C', linestyle='--',
                    label=f'Premium: ${premium_bad:,.2f}')
        ax2.legend(fontsize=10, loc='upper left')  # Move legend to avoid image

        # Add dollar value labels
        for bar, value in zip(bars2, bad_values):
            percentage = value / premium_bad * 100
            ax2.text(bar.get_x() + bar.get_width() / 2, value + (y_max * 0.02),
                     f'${value:,.0f}\n({percentage:.1f}%)',
                     ha='center', va='bottom',
                     fontsize=9)

        # Format y-axis with commas
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))

        # 3. GOOD DRIVER PIE CHART (BOTTOM LEFT)
        wedges, texts, autotexts = ax3.pie(good_values, labels=components, colors=colors,
                                           autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})

        # Make text more readable
        for text in texts:
            text.set_fontweight('bold')

        ax3.set_title(f'{first_cohort_name} Premium: ${premium_good:,.2f}', fontsize=12)

        # 4. BAD DRIVER PIE CHART (BOTTOM RIGHT)
        wedges, texts, autotexts = ax4.pie(bad_values, labels=components, colors=colors,
                                           autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})

        # Make text more readable
        for text in texts:
            text.set_fontweight('bold')

        ax4.set_title(f'{second_cohort_name} Premium: ${premium_bad:,.2f}', fontsize=12)

        # Set aspect equal for pie charts
        ax3.set_aspect('equal')
        ax4.set_aspect('equal')

        # Premium difference calculation
        premium_diff = premium_bad - premium_good
        premium_ratio = premium_bad / premium_good

        # Add premium difference as a simple text item at the top
        # Use a more compact and less overwhelming design
        props = dict(boxstyle='round,pad=0.3', facecolor='#3498DB', alpha=0.9)
        fig.text(0.5, 0.98,
                 f"Premium Difference: ${premium_diff:,.2f} ({premium_ratio:.1f}x higher for {second_cohort_name})",
                 ha='center', va='top', fontsize=11,
                 color='white', bbox=props)

        # Try to add rapper images inside the bar charts (LARGER SIZE)
        try:
            # Determine image paths
            good_image_path = os.path.join("modules", good_driver_image)
            bad_image_path = os.path.join("modules", f"{bad_driver_name.lower()}.jpeg")

            if os.path.exists(good_image_path) and os.path.exists(bad_image_path):
                # Load good driver image - place in the bar chart with LARGER SIZE
                good_img = plt.imread(good_image_path)
                imagebox_good = OffsetImage(good_img, zoom=0.40, alpha=0.8)  # Increased from 0.25 to 0.40
                # Position in upper right of the good driver chart, with slight adjustment
                ab_good = AnnotationBbox(imagebox_good, (0.70, 0.70),  # Adjusted from 0.85,0.75 to 0.70,0.70
                                         frameon=True,  # Add frame
                                         box_alignment=(0.5, 0.5),  # Center alignment
                                         xycoords='axes fraction',
                                         pad=0.2,
                                         bboxprops=dict(facecolor='white', alpha=0.6, boxstyle='round'))
                ax1.add_artist(ab_good)

                # Load bad driver image - place in the bar chart with LARGER SIZE
                bad_img = plt.imread(bad_image_path)
                imagebox_bad = OffsetImage(bad_img, zoom=0.40, alpha=0.8)  # Increased from 0.25 to 0.40
                # Position in upper right of the bad driver chart with slight adjustment
                ab_bad = AnnotationBbox(imagebox_bad, (0.70, 0.70),  # Adjusted from 0.85,0.75 to 0.70,0.70
                                        frameon=True,  # Add frame
                                        box_alignment=(0.5, 0.5),  # Center alignment
                                        xycoords='axes fraction',
                                        pad=0.2,
                                        bboxprops=dict(facecolor='white', alpha=0.6, boxstyle='round'))
                ax2.add_artist(ab_bad)
            else:
                print(f"Warning: Image file not found. Looking for: {good_image_path} and {bad_image_path}")
        except Exception as e:
            print(f"Error adding images: {e}")

        # Create formula text box
        formula_text = f"Premium Calculation Formula:\n\n" \
                       f"Premium = Expected Loss / (1 - Expense% - Risk%)\n\n" \
                       f"Where:\n" \
                       f"• Expected Loss = Frequency × Severity\n" \
                       f"• Expense Ratio = {expense_ratio:.0%}\n" \
                       f"• Risk Margin = {risk_margin_ratio:.0%}"

        # Add formula text to figure
        props = dict(boxstyle='round', facecolor='#F2F4F4', ec='#BDC3C7', alpha=0.9)
        fig.text(0.5, 0.02, formula_text, fontsize=11,
                 ha='center', va='bottom', bbox=props)

        # The automatic adjustments don't work well with GridSpec
        # So we won't use tight_layout() or subplots_adjust() here

        # Key statistics to return
        stats = {
            'expected_loss': expected_loss_good,
            'expenses': expenses_good,
            'risk_margin': risk_margin_good,
            'premium': premium_good,
            'loading_factor': loading_factor_good,
            'expected_loss_bad': expected_loss_bad,
            'expenses_bad': expenses_bad,
            'risk_margin_bad': risk_margin_bad,
            'premium_bad': premium_bad,
            'loading_factor_bad': loading_factor_bad,
            'good_driver_image': good_driver_image,
            'good_driver_name': good_driver_name,
            'bad_driver_name': bad_driver_name,
            'first_cohort_name': first_cohort_name,
            'second_cohort_name': second_cohort_name
        }

        return fig, stats

    # Original function for compatibility
    else:
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Rest of the implementation would be similar
        plt.show()

        # Display insurance interpretation
        print("\nInsurance Interpretation:")
        print(
            f"• {first_cohort_name} Est. Accident Frequency: {accident_frequency:.1%} (probability of claim per year)")
        print(
            f"• {first_cohort_name} Est. Average Claim Severity: ${claim_severity:,.0f} (average cost when a claim occurs)")
        print(f"• {first_cohort_name} Expected Loss: ${expected_loss_good:.2f} (pure cost of risk)")
        print(
            f"• {first_cohort_name} Expenses: ${expenses_good:.2f} ({expense_ratio:.0%} of premium for administration, commissions, etc.)")
        print(
            f"• {first_cohort_name} Risk Margin: ${risk_margin_good:.2f} ({risk_margin_ratio:.0%} of premium for profit and uncertainty)")
        print(f"• {first_cohort_name} Final Premium: ${premium_good:.2f}")
        print(f"• {second_cohort_name} Final Premium: ${premium_bad:.2f}")
        print("\nThis is the base premium before applying individual rating factors like age, driving history, etc.")