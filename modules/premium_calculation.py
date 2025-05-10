import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def demonstrate_premium_calculation(accident_frequency=0.05, claim_severity=8000, return_fig=False):
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

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object (if return_fig is True)
    stats : dict
        Key statistics (if return_fig is True)
    """
    # Calculate components
    expected_loss = accident_frequency * claim_severity
    expense_ratio = 0.25  # Fixed at 25% of premium
    risk_margin_ratio = 0.05  # Fixed at 5% of premium

    # Premium components (solving the equation)
    # Premium = Expected Loss + Expense Ratio × Premium + Risk Margin × Premium
    # Premium = Expected Loss / (1 - Expense Ratio - Risk Margin)
    premium = expected_loss / (1 - expense_ratio - risk_margin_ratio)
    expenses = premium * expense_ratio
    risk_margin = premium * risk_margin_ratio

    # Loading factor
    loading_factor = premium / expected_loss

    # For Shiny integration
    if return_fig:
        # Create figure
        fig = Figure(figsize=(12, 10))

        # Create subplots
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        # Plot 1: Premium components
        components = ['Expected Loss', 'Expenses', 'Risk Margin']
        values = [expected_loss, expenses, risk_margin]
        colors = ['blue', 'orange', 'green']

        bars = ax1.bar(components, values, color=colors, alpha=0.7)
        ax1.set_title('Premium Components', fontsize=14)
        ax1.set_ylabel('Amount ($)', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)

        # Add a line for total premium
        ax1.axhline(premium, color='red', linestyle='--', label=f'Total Premium: ${premium:.2f}')
        ax1.legend(fontsize=12)

        # Add text annotations for each component
        for bar, value, component in zip(bars, values, components):
            percentage = value / premium * 100
            ax1.text(bar.get_x() + bar.get_width() / 2, value / 2,
                     f'${value:.2f}\n({percentage:.1f}%)',
                     ha='center', va='center',
                     color='white' if value > 100 else 'black',
                     fontsize=11)

        # Plot 2: Breakdown in pie chart
        ax2.pie(values, labels=components, colors=colors, autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 12})
        ax2.set_title(f'Premium Breakdown (Total: ${premium:.2f})', fontsize=14)

        # Create formula text at the side
        formula_text = f"Premium Calculation:\n\n" \
                       f"• Expected Loss = Frequency × Severity\n" \
                       f"  = {accident_frequency:.1%} × ${claim_severity:,.0f}\n" \
                       f"  = ${expected_loss:.2f}\n\n" \
                       f"• Premium = Expected Loss / (1 - Expense% - Risk%)\n" \
                       f"  = ${expected_loss:.2f} / (1 - {expense_ratio:.0%} - {risk_margin_ratio:.0%})\n" \
                       f"  = ${premium:.2f}"

        # Add the text as an annotation instead of a separate axis
        fig.text(0.75, 0.3, formula_text, fontsize=12,
                 verticalalignment='center', horizontalalignment='left',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

        # Adjust spacing
        fig.subplots_adjust(hspace=0.4)

        # Key statistics to return
        stats = {
            'expected_loss': expected_loss,
            'expenses': expenses,
            'risk_margin': risk_margin,
            'premium': premium,
            'loading_factor': loading_factor
        }

        return fig, stats

    # Original function for compatibility
    else:
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Plot 1: Premium components
        components = ['Expected Loss', 'Expenses', 'Risk Margin']
        values = [expected_loss, expenses, risk_margin]
        colors = ['blue', 'orange', 'green']

        bars = ax1.bar(components, values, color=colors, alpha=0.7)
        ax1.set_title('Premium Components', fontsize=14)
        ax1.set_ylabel('Amount ($)', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)

        # Add a line for total premium
        ax1.axhline(premium, color='red', linestyle='--', label=f'Total Premium: ${premium:.2f}')
        ax1.legend(fontsize=12)

        # Add text annotations for each component
        for bar, value, component in zip(bars, values, components):
            percentage = value / premium * 100
            ax1.text(bar.get_x() + bar.get_width() / 2, value / 2,
                     f'${value:.2f}\n({percentage:.1f}%)',
                     ha='center', va='center',
                     color='white' if value > 100 else 'black',
                     fontsize=11)

        # Plot 2: Breakdown in pie chart
        ax2.pie(values, labels=components, colors=colors, autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 12})
        ax2.set_title(f'Premium Breakdown (Total: ${premium:.2f})', fontsize=14)

        # Create a separate axis for the formula text
        formula_ax = plt.axes([0.80, 0.15, 0.25, 0.25])
        formula_ax.axis('off')  # Hide axis

        # Formula text content
        formula_text = f"Premium Calculation:\n\n" \
                       f"• Expected Loss = Frequency × Severity\n" \
                       f"  = {accident_frequency:.1%} × ${claim_severity:,.0f}\n" \
                       f"  = ${expected_loss:.2f}\n\n" \
                       f"• Premium = Expected Loss / (1 - Expense% - Risk%)\n" \
                       f"  = ${expected_loss:.2f} / (1 - {expense_ratio:.0%} - {risk_margin_ratio:.0%})\n" \
                       f"  = ${premium:.2f}"

        # Add the formula text to the axis
        formula_ax.text(0, 0.5, formula_text, fontsize=12,
                        verticalalignment='center', horizontalalignment='left',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

        # Adjust spacing
        plt.subplots_adjust(hspace=0.4)
        plt.show()

        # Display insurance interpretation
        print("\nInsurance Interpretation:")
        print(f"• Accident Frequency: {accident_frequency:.1%} (probability of claim per year)")
        print(f"• Average Claim Severity: ${claim_severity:,.0f} (average cost when a claim occurs)")
        print(f"• Expected Loss: ${expected_loss:.2f} (pure cost of risk)")
        print(f"• Expenses: ${expenses:.2f} ({expense_ratio:.0%} of premium for administration, commissions, etc.)")
        print(f"• Risk Margin: ${risk_margin:.2f} ({risk_margin_ratio:.0%} of premium for profit and uncertainty)")
        print(f"• Final Premium: ${premium:.2f}")
        print("\nThis is the base premium before applying individual rating factors like age, driving history, etc.")