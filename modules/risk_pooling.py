import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def demonstrate_risk_pooling(accident_probability=0.05, num_policyholders=100, seed=42, return_fig=False):
    """
    Demonstrates the concept of risk pooling in insurance

    Parameters:
    -----------
    accident_probability : float
        The probability of an accident
    num_policyholders : int
        The number of policyholders
    seed : int
        Random seed for reproducibility
    return_fig : bool
        If True, returns the figure and stats for Shiny integration

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object (if return_fig is True)
    stats : dict
        Key statistics (if return_fig is True)
    """
    # Fixed claim amount at $20,000
    CLAIM_AMOUNT = 20000

    # Set random seed for consistent results
    np.random.seed(seed)

    # Run the simulation - generate random accidents
    accidents = np.random.random(num_policyholders) < accident_probability

    # Calculate results
    individual_costs = np.where(accidents, CLAIM_AMOUNT, 0)
    total_losses = np.sum(individual_costs)
    fair_premium = accident_probability * CLAIM_AMOUNT
    pool_premium_total = fair_premium * num_policyholders

    # Calculate stats
    num_with_loss = np.sum(accidents)
    percent_with_loss = np.mean(accidents) * 100
    pool_performance = total_losses / pool_premium_total

    # For Shiny integration
    if return_fig:
        # Create figure
        fig = Figure(figsize=(14, 7))

        # Create subplots
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # Plot 1: Individual outcomes with improved visualization
        # Always show all policyholders for complete consistency with pooled outcomes
        display_n = num_policyholders
        outcomes_label = f'Individual outcomes (n={display_n})'

        # Blue bar chart for individual outcomes
        ax1.bar(
            ['Without Insurance'],
            [CLAIM_AMOUNT],
            color='lightblue',
            alpha=0.3,
            width=0.6,
            label='Potential loss amount'
        )

        # Overlay scatter plot showing actual outcomes
        x_positions = np.ones(display_n) * 0  # All points at x=0 ("Without Insurance")
        y_positions = individual_costs[:display_n]  # Each person's actual outcome

        # Add jitter to x positions for better visualization
        x_jitter = np.random.uniform(-0.2, 0.2, size=display_n)
        x_positions += x_jitter

        # Plot the actual outcomes as scatter points
        ax1.scatter(
            x_positions,
            y_positions,
            color='blue',
            alpha=0.7,
            label=outcomes_label
        )

        # Add a bar for premium with insurance
        ax1.bar(
            ['With Insurance'],
            [fair_premium],
            color='green',
            alpha=0.7,
            width=0.6,
            label='Insurance premium'
        )

        # Calculate statistics for displayed individuals only
        displayed_accidents = accidents[:display_n]
        displayed_with_loss = np.sum(displayed_accidents)
        
        # Annotation showing how many people experienced a loss
        ax1.annotate(
            f"{displayed_with_loss} out of {display_n} people\nexperienced a ${CLAIM_AMOUNT:,} loss",
            xy=(0, CLAIM_AMOUNT / 2),
            xytext=(0, CLAIM_AMOUNT * 0.7),
            ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8)
        )

        # Annotation explaining insurance premium
        ax1.annotate(
            f"Everyone pays\n${fair_premium:,.0f}",
            xy=(1, fair_premium / 2),
            xytext=(1, fair_premium * 1.5),
            ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.8)
        )

        ax1.set_ylabel('Cost ($)')
        ax1.set_title(f'Individual Risk Outcomes vs Pooled Outcomes')
        ax1.grid(axis='y', alpha=0.3)
        ax1.legend(loc='upper center')

        # Set y-axis limit to ensure visibility of premium
        ax1.set_ylim(0, CLAIM_AMOUNT * 1.1)

        # Plot 2: Pooled outcome (insurer perspective)
        ax2.bar(['Premiums Collected', 'Actual Losses'],
                [pool_premium_total, total_losses],
                color=['green', 'blue'], alpha=0.7)
        ax2.set_ylabel('Amount ($)')
        ax2.set_title(f'Insurer\'s Perspective')

        # Calculate expected maximum loss at 99% confidence level based on binomial distribution
        # This helps keep the y-axis consistent across different simulations
        p = accident_probability
        n = num_policyholders
        # Using normal approximation to binomial with continuity correction for 99% CI (2.576 is z-score for 99%)
        max_expected_claims = n * p + 2.576 * np.sqrt(n * p * (1 - p)) + 0.5
        max_expected_loss = max_expected_claims * CLAIM_AMOUNT

        # Set y-axis to use the consistent 99% CI maximum
        y_max = max(max_expected_loss, total_losses) * 1.1  # Add 10% margin
        ax2.set_ylim(0, y_max)

        ax2.grid(True, alpha=0.3)

        # Add explanatory text
        performance_text = "Surplus" if pool_performance < 1 else "Deficit"
        performance_color = "green" if pool_performance < 1 else "red"

        ax2.text(0.5, 0.95,
                 f"Expected losses: ${pool_premium_total:,.0f}\nActual losses: ${total_losses:,.0f}\n{performance_text}: ${abs(pool_premium_total - total_losses):,.0f}",
                 transform=ax2.transAxes, ha='center', va='top',
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.8))

        # Add annotation for ratio
        ax2.text(1, total_losses + 0.05 * max(pool_premium_total, total_losses),
                 f"Actual/Expected: {pool_performance:.2f}", ha='center', color=performance_color)

        # Remove seed text from figure
        # fig.text(0.5, 0.01, f"Simulation Seed: {seed}", ha='center',
        #          fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))

        # Use subplots_adjust for more reliable layout
        fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1, wspace=0.3)

        # Return the figure and key statistics
        displayed_percent_with_loss = (displayed_with_loss / display_n) * 100 if display_n > 0 else 0
        stats = {
            'num_with_loss': num_with_loss,
            'percent_with_loss': percent_with_loss,
            'displayed_num_with_loss': displayed_with_loss,
            'displayed_percent_with_loss': displayed_percent_with_loss,
            'display_n': display_n,
            'fair_premium': fair_premium,
            'total_losses': total_losses,
            'pool_premium_total': pool_premium_total,
            'pool_performance': pool_performance,
            'seed': seed  # Include seed in stats
        }

        return fig, stats

    # Original function for compatibility
    else:
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

        # Plot 1: Individual outcomes with improved visualization
        # Always show all policyholders for complete consistency with pooled outcomes
        display_n = num_policyholders
        outcomes_label = f'Individual outcomes (n={display_n})'

        # Blue bar chart for individual outcomes
        ax1.bar(
            ['Without Insurance'],
            [CLAIM_AMOUNT],
            color='lightblue',
            alpha=0.3,
            width=0.6,
            label='Potential loss amount'
        )

        # Overlay scatter plot showing actual outcomes
        x_positions = np.ones(display_n) * 0  # All points at x=0 ("Without Insurance")
        y_positions = individual_costs[:display_n]  # Each person's actual outcome

        # Add jitter to x positions for better visualization
        x_jitter = np.random.uniform(-0.2, 0.2, size=display_n)
        x_positions += x_jitter

        # Plot the actual outcomes as scatter points
        ax1.scatter(
            x_positions,
            y_positions,
            color='blue',
            alpha=0.7,
            label=outcomes_label
        )

        # Add a bar for premium with insurance
        ax1.bar(
            ['With Insurance'],
            [fair_premium],
            color='green',
            alpha=0.7,
            width=0.6,
            label='Insurance premium'
        )

        # Calculate statistics for displayed individuals only
        displayed_accidents = accidents[:display_n]
        displayed_with_loss = np.sum(displayed_accidents)
        
        # Annotation showing how many people experienced a loss
        ax1.annotate(
            f"{displayed_with_loss} out of {display_n} people\nexperienced a ${CLAIM_AMOUNT:,} loss",
            xy=(0, CLAIM_AMOUNT / 2),
            xytext=(0, CLAIM_AMOUNT * 0.7),
            ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8)
        )

        # Annotation explaining insurance premium
        ax1.annotate(
            f"Everyone pays\n${fair_premium:,.0f}",
            xy=(1, fair_premium / 2),
            xytext=(1, fair_premium * 1.5),
            ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.8)
        )

        ax1.set_ylabel('Cost ($)')
        ax1.set_title(f'Individual Risk Outcomes vs Pooled Outcomes (Seed: {seed})')
        ax1.grid(axis='y', alpha=0.3)
        ax1.legend(loc='upper center')

        # Set y-axis limit to ensure visibility of premium
        ax1.set_ylim(0, CLAIM_AMOUNT * 1.1)

        # Plot 2: Pooled outcome (insurer perspective)
        ax2.bar(['Premiums Collected', 'Actual Losses'],
                [pool_premium_total, total_losses],
                color=['green', 'blue'], alpha=0.7)
        ax2.set_ylabel('Amount ($)')
        ax2.set_title(f'Insurer\'s Perspective (Seed: {seed})')
        ax2.grid(True, alpha=0.3)

        # Add explanatory text
        performance_text = "Surplus" if pool_performance < 1 else "Deficit"
        performance_color = "green" if pool_performance < 1 else "red"

        ax2.text(0.5, 0.95,
                 f"Expected losses: ${pool_premium_total:,.0f}\nActual losses: ${total_losses:,.0f}\n{performance_text}: ${abs(pool_premium_total - total_losses):,.0f}",
                 transform=ax2.transAxes, ha='center', va='top',
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.8))

        # Add annotation for ratio
        ax2.text(1, total_losses + 0.05 * max(pool_premium_total, total_losses),
                 f"Actual/Expected: {pool_performance:.2f}", ha='center', color=performance_color)

        # Add a text annotation with the seed value
        fig.text(0.5, 0.01, f"Simulation Seed: {seed}", ha='center',
                 fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))

        # Use subplots_adjust for more reliable layout
        plt.subplots_adjust(left=0.08, right=0.95, top=0.9, bottom=0.15, wspace=0.3)
        plt.show()

        # Display insurance interpretation
        print("\nInsurance Interpretation:")
        print(f"• Simulation Seed: {seed}")
        print(f"• Individual Risk: Each person has a {accident_probability:.1%} chance of a ${CLAIM_AMOUNT:,.0f} loss.")
        print(
            f"• Without Insurance: {num_with_loss} people ({percent_with_loss:.1f}%) faced a ${CLAIM_AMOUNT:,.0f} loss in this simulation.")
        print(f"• With Insurance: Everyone pays a premium of ${fair_premium:.0f}.")
        print(
            f"• Risk Pooling Result: The insurer collected ${pool_premium_total:,.0f} and paid ${total_losses:,.0f} in claims.")

        if pool_performance < 1:
            print(
                f"• This year the insurance pool had a ${abs(pool_premium_total - total_losses):,.0f} surplus (collected more than paid out).")
            print(f"• The surplus can be held as capital to handle future years when claims exceed premiums.")
        else:
            print(
                f"• This year the insurance pool had a ${abs(pool_premium_total - total_losses):,.0f} deficit (paid out more than collected).")
            print(f"• The deficit must be covered by the insurer's capital reserves.")

        print(f"\n• Key Insight: As the number of policyholders increases, the 'Actual/Expected' ratio approaches 1.0,")
        print(f"  making the insurance pool's results more predictable and stable.")