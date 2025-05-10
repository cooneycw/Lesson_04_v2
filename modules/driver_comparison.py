import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from scipy.stats import lognorm


def demonstrate_driver_comparison(base_frequency=0.05, base_severity=8000, bad_driver_freq_multiplier=3.0,
                                  bad_driver_severity_multiplier=2.0, seed=42, return_fig=False,
                                  good_driver_image="drake.jpeg"):
    """
    Demonstrates the difference in outcomes between good and bad drivers

    Parameters:
    -----------
    base_frequency : float
        Base accident frequency for good drivers
    base_severity : float
        Base accident severity for good drivers
    bad_driver_freq_multiplier : float
        How much more frequently bad drivers have accidents
    bad_driver_severity_multiplier : float
        How much more severe bad drivers' accidents are
    seed : int
        Random seed for reproducibility
    return_fig : bool
        If True, returns the figure and stats for Shiny integration
    good_driver_image : str
        Image filename to use for the good driver (either "drake.jpeg" or "kendrick.jpeg")

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

    # Define parameters for each driver type
    bad_driver_frequency = base_frequency * bad_driver_freq_multiplier
    bad_driver_severity = base_severity * bad_driver_severity_multiplier

    # Number of drivers to simulate
    num_good_drivers = 200
    num_bad_drivers = 200

    # Parameters for lognormal distribution
    good_sigma = 0.4  # Smaller sigma for good drivers (less variance)
    bad_sigma = 0.6  # Larger sigma for bad drivers (more variance)

    # Calculate mu so that the median of the lognormal is our target severity
    good_mu = np.log(base_severity) - 0.5 * good_sigma ** 2
    bad_mu = np.log(bad_driver_severity) - 0.5 * bad_sigma ** 2

    # Generate individual driver frequencies
    good_driver_frequencies = np.random.normal(base_frequency, base_frequency * 0.3, num_good_drivers)
    good_driver_frequencies = np.maximum(good_driver_frequencies, 0.001)  # Minimum 0.1% frequency

    bad_driver_frequencies = np.random.normal(bad_driver_frequency, bad_driver_frequency * 0.3, num_bad_drivers)
    bad_driver_frequencies = np.maximum(bad_driver_frequencies, 0.001)  # Minimum 0.1% frequency

    # Generate individual driver severities (using lognormal)
    good_driver_severities = lognorm.rvs(good_sigma, scale=np.exp(good_mu), size=num_good_drivers)
    bad_driver_severities = lognorm.rvs(bad_sigma, scale=np.exp(bad_mu), size=num_bad_drivers)

    # Calculate statistics
    good_avg_frequency = np.mean(good_driver_frequencies)
    bad_avg_frequency = np.mean(bad_driver_frequencies)

    good_avg_severity = np.mean(good_driver_severities)
    bad_avg_severity = np.mean(bad_driver_severities)

    good_total_losses = good_avg_frequency * good_avg_severity * num_good_drivers
    bad_total_losses = bad_avg_frequency * bad_avg_severity * num_bad_drivers

    # For Shiny integration
    if return_fig:
        # Create figure - NARROWED BY 25%
        fig = Figure(figsize=(10.5, 10))  # Changed from 14 to 10.5 width (25% reduction)

        # Create subplots - just use one main plot and one for statistics
        ax1 = fig.add_subplot(111)  # Main scatterplot

        # Plot: Scatter plot of driver risk profiles
        # Add small jitter to separate overlapping points
        jitter_x_good = np.random.normal(0, 0.001, num_good_drivers)
        jitter_x_bad = np.random.normal(0, 0.001, num_bad_drivers)

        # Scatter plot for good drivers
        ax1.scatter(
            good_driver_frequencies + jitter_x_good,
            good_driver_severities,
            color='green',
            alpha=0.7,
            s=70,
            label=f'{good_driver_name} (Good Driver)',
            edgecolors='darkgreen'
        )

        # Scatter plot for bad drivers
        ax1.scatter(
            bad_driver_frequencies + jitter_x_bad,
            bad_driver_severities,
            color='red',
            alpha=0.7,
            s=70,
            label=f'{bad_driver_name} (Bad Driver)',
            edgecolors='darkred'
        )

        # Add center points for each cluster
        ax1.scatter(
            good_avg_frequency,
            good_avg_severity,
            color='darkgreen',
            s=150,
            marker='*',
            label=f'{good_driver_name} Average'
        )

        ax1.scatter(
            bad_avg_frequency,
            bad_avg_severity,
            color='darkred',
            s=150,
            marker='*',
            label=f'{bad_driver_name} Average'
        )

        # Add frequency and severity lines for reference
        ax1.axvline(x=base_frequency, color='lightgreen', linestyle='--', alpha=0.5)
        ax1.axvline(x=bad_driver_frequency, color='lightcoral', linestyle='--', alpha=0.5)

        ax1.axhline(y=base_severity, color='lightgreen', linestyle='--', alpha=0.5)
        ax1.axhline(y=bad_driver_severity, color='lightcoral', linestyle='--', alpha=0.5)

        # Annotations for the lines
        ax1.text(base_frequency, ax1.get_ylim()[0] * 1.05, f"{good_driver_name} Frequency: {base_frequency:.1%}",
                 color='darkgreen', ha='center', va='bottom', rotation=90)
        ax1.text(bad_driver_frequency, ax1.get_ylim()[0] * 1.05,
                 f"{bad_driver_name} Frequency: {bad_driver_frequency:.1%}",
                 color='darkred', ha='center', va='bottom', rotation=90)

        # Format axes
        ax1.set_xlabel('Accident Frequency (probability per year)', fontsize=12)
        ax1.set_ylabel('Average Claim Amount ($)', fontsize=12)
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
            f"{good_driver_name} (Good Driver):\n"
            f"• Avg Frequency: {good_avg_frequency:.1%}\n"
            f"• Avg Claim Amount: ${good_avg_severity:,.0f}\n"
            f"• Total Expected Loss: ${good_total_losses:,.0f}\n\n"
            f"{bad_driver_name} (Bad Driver):\n"
            f"• Avg Frequency: {bad_avg_frequency:.1%} ({bad_avg_frequency / good_avg_frequency:.1f}x higher)\n"
            f"• Avg Claim Amount: ${bad_avg_severity:,.0f} ({bad_avg_severity / good_avg_severity:.1f}x higher)\n"
            f"• Total Expected Loss: ${bad_total_losses:,.0f} ({bad_total_losses / good_total_losses:.1f}x higher)"
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
            'good_avg_frequency': good_avg_frequency,
            'bad_avg_frequency': bad_avg_frequency,
            'good_avg_severity': good_avg_severity,
            'bad_avg_severity': bad_avg_severity,
            'good_total_losses': good_total_losses,
            'bad_total_losses': bad_total_losses,
            'loss_multiplier': bad_total_losses / good_total_losses,
            'freq_multiplier': bad_avg_frequency / good_avg_frequency,
            'severity_multiplier': bad_avg_severity / good_avg_severity,
            'good_driver_image': good_driver_image,
            'good_driver_name': good_driver_name,
            'bad_driver_name': bad_driver_name
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
        print(f"• {good_driver_name}: {good_avg_frequency:.1%} accident rate, ${good_avg_severity:,.2f} avg severity")
        print(f"• {bad_driver_name}: {bad_avg_frequency:.1%} accident rate, ${bad_avg_severity:,.2f} avg severity")
        print(f"• {good_driver_name} total loss: ${good_total_losses:,.0f}")
        print(
            f"• {bad_driver_name} total loss: ${bad_total_losses:,.0f} ({bad_total_losses / good_total_losses:.1f}x higher)")