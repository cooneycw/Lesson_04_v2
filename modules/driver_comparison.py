import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from scipy.stats import lognorm


def demonstrate_driver_comparison(base_frequency=0.05, base_severity=8000, bad_driver_freq_multiplier=3.0,
                                  bad_driver_severity_multiplier=2.0, seed=42, return_fig=False,
                                  good_driver_image="drake.jpeg"):
    """
    Demonstrates the difference in outcomes between driver cohorts

    Parameters:
    -----------
    base_frequency : float
        Base accident frequency for first cohort
    base_severity : float
        Base accident severity for first cohort
    bad_driver_freq_multiplier : float
        How much more frequently second cohort has accidents
    bad_driver_severity_multiplier : float
        How much more severe second cohort's accidents are
    seed : int
        Random seed for reproducibility
    return_fig : bool
        If True, returns the figure and stats for Shiny integration
    good_driver_image : str
        Image filename to use for the first cohort (either "drake.jpeg" or "kendrick.jpeg")

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object (if return_fig is True)
    stats : dict
        Key statistics (if return_fig is True)
    """
    # Set random seed for reproducibility
    np.random.seed(seed)

    # Extract driver names from image filename
    good_driver_name = good_driver_image.split('.')[0].capitalize()
    bad_driver_name = "Kendrick" if good_driver_name == "Drake" else "Drake"

    # Use specific cohort names
    first_cohort_name = f"{good_driver_name} Cohort"
    second_cohort_name = f"{bad_driver_name} Cohort"

    # Define parameters for each driver type
    second_cohort_frequency = base_frequency * bad_driver_freq_multiplier
    second_cohort_severity = base_severity * bad_driver_severity_multiplier

    # Number of drivers to simulate
    num_first_cohort = 200
    num_second_cohort = 200

    # Parameters for lognormal distribution
    first_sigma = 0.4  # Smaller sigma for first cohort (less variance)
    second_sigma = 0.6  # Larger sigma for second cohort (more variance)

    # Calculate mu so that the median of the lognormal is our target severity
    first_mu = np.log(base_severity) - 0.5 * first_sigma ** 2
    second_mu = np.log(second_cohort_severity) - 0.5 * second_sigma ** 2

    # Generate individual driver frequencies
    first_cohort_frequencies = np.random.normal(base_frequency, base_frequency * 0.3, num_first_cohort)
    first_cohort_frequencies = np.maximum(first_cohort_frequencies, 0.001)  # Minimum 0.1% frequency

    second_cohort_frequencies = np.random.normal(second_cohort_frequency, second_cohort_frequency * 0.3,
                                                 num_second_cohort)
    second_cohort_frequencies = np.maximum(second_cohort_frequencies, 0.001)  # Minimum 0.1% frequency

    # Generate individual driver severities (using lognormal)
    first_cohort_severities = lognorm.rvs(first_sigma, scale=np.exp(first_mu), size=num_first_cohort)
    second_cohort_severities = lognorm.rvs(second_sigma, scale=np.exp(second_mu), size=num_second_cohort)

    # Calculate statistics
    first_avg_frequency = np.mean(first_cohort_frequencies)
    second_avg_frequency = np.mean(second_cohort_frequencies)

    first_avg_severity = np.mean(first_cohort_severities)
    second_avg_severity = np.mean(second_cohort_severities)

    first_total_losses = first_avg_frequency * first_avg_severity * num_first_cohort
    second_total_losses = second_avg_frequency * second_avg_severity * num_second_cohort

    # For Shiny integration
    if return_fig:
        # Create figure - NARROWED BY 25%
        fig = Figure(figsize=(10.5, 10))  # Changed from 14 to 10.5 width (25% reduction)

        # Create subplots - just use one main plot and one for statistics
        ax1 = fig.add_subplot(111)  # Main scatterplot

        # Plot: Scatter plot of driver risk profiles
        # Add small jitter to separate overlapping points
        jitter_x_first = np.random.normal(0, 0.001, num_first_cohort)
        jitter_x_second = np.random.normal(0, 0.001, num_second_cohort)

        # Scatter plot for first cohort
        ax1.scatter(
            first_cohort_frequencies + jitter_x_first,
            first_cohort_severities,
            color='green',
            alpha=0.7,
            s=70,
            label=f'{first_cohort_name}',
            edgecolors='darkgreen'
        )

        # Scatter plot for second cohort
        ax1.scatter(
            second_cohort_frequencies + jitter_x_second,
            second_cohort_severities,
            color='red',
            alpha=0.7,
            s=70,
            label=f'{second_cohort_name}',
            edgecolors='darkred'
        )

        # Add center points for each cluster
        ax1.scatter(
            first_avg_frequency,
            first_avg_severity,
            color='darkgreen',
            s=150,
            marker='*',
            label=f'{first_cohort_name} Average'
        )

        ax1.scatter(
            second_avg_frequency,
            second_avg_severity,
            color='darkred',
            s=150,
            marker='*',
            label=f'{second_cohort_name} Average'
        )

        # Add frequency and severity lines for reference
        ax1.axvline(x=base_frequency, color='lightgreen', linestyle='--', alpha=0.5)
        ax1.axvline(x=second_cohort_frequency, color='lightcoral', linestyle='--', alpha=0.5)

        ax1.axhline(y=base_severity, color='lightgreen', linestyle='--', alpha=0.5)
        ax1.axhline(y=second_cohort_severity, color='lightcoral', linestyle='--', alpha=0.5)

        # Annotations for the lines
        ax1.text(base_frequency, ax1.get_ylim()[0] * 1.05, f"{first_cohort_name} Frequency: {base_frequency:.1%}",
                 color='darkgreen', ha='center', va='bottom', rotation=90)
        ax1.text(second_cohort_frequency, ax1.get_ylim()[0] * 1.05,
                 f"{second_cohort_name} Frequency: {second_cohort_frequency:.1%}",
                 color='darkred', ha='center', va='bottom', rotation=90)

        # Format axes with updated terminology
        ax1.set_xlabel('Est. Accident Frequency (probability per year)', fontsize=12)
        ax1.set_ylabel('Est. Average Claim Amount ($)', fontsize=12)
        ax1.set_title('Driver Risk Profiles: Frequency vs Claim Amount', fontsize=14)
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)

        # Set x-axis as percentage
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))

        # Set y-axis format to display dollar amounts
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))

        # Add summary statistics in a box - MOVED TO NOT OVERLAP WITH CHART
        summary_text = (
            f"Risk Profile Comparison\n\n"
            f"{first_cohort_name}:\n"
            f"• Avg Frequency: {first_avg_frequency:.1%}\n"
            f"• Avg Claim Amount: ${first_avg_severity:,.0f}\n"
            f"• Total Expected Loss: ${first_total_losses:,.0f}\n\n"
            f"{second_cohort_name}:\n"
            f"• Avg Frequency: {second_avg_frequency:.1%} ({second_avg_frequency / first_avg_frequency:.1f}x higher)\n"
            f"• Avg Claim Amount: ${second_avg_severity:,.0f} ({second_avg_severity / first_avg_severity:.1f}x higher)\n"
            f"• Total Expected Loss: ${second_total_losses:,.0f} ({second_total_losses / first_total_losses:.1f}x higher)"
        )

        # Place text box on the right side (LEFT JUSTIFIED)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
        ax1.text(1.05, 0.5, summary_text, fontsize=12,
                 verticalalignment='center', horizontalalignment='left',
                 bbox=props, transform=ax1.transAxes)

        # Adjust layout to make space for the text box
        fig.tight_layout()
        fig.subplots_adjust(right=0.75)  # Make room for the summary box on the right

        # Stats to return
        stats = {
            'good_avg_frequency': first_avg_frequency,
            'bad_avg_frequency': second_avg_frequency,
            'good_avg_severity': first_avg_severity,
            'bad_avg_severity': second_avg_severity,
            'good_total_losses': first_total_losses,
            'bad_total_losses': second_total_losses,
            'loss_multiplier': second_total_losses / first_total_losses,
            'freq_multiplier': second_avg_frequency / first_avg_frequency,
            'severity_multiplier': second_avg_severity / first_avg_severity,
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
        fig = plt.figure(figsize=(14, 10))

        # Rest of the implementation would be similar to the return_fig=True case
        # This is just a placeholder for compatibility
        plt.show()

        # Print statistics
        print("\nDriver Comparison Interpretation:")
        print(
            f"• {first_cohort_name}: {first_avg_frequency:.1%} accident rate, ${first_avg_severity:,.2f} avg severity")
        print(
            f"• {second_cohort_name}: {second_avg_frequency:.1%} accident rate, ${second_avg_severity:,.2f} avg severity")
        print(f"• {first_cohort_name} total loss: ${first_total_losses:,.0f}")
        print(
            f"• {second_cohort_name} total loss: ${second_total_losses:,.0f} ({second_total_losses / first_total_losses:.1f}x higher)")