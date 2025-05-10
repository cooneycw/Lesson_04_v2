# Insurance Fundamentals - Shiny App

This is a Shiny for Python application demonstrating key insurance concepts through interactive visualizations.

## Features

The app includes three interactive modules:

1. **Risk Pooling**: Shows how insurance distributes risk across many policyholders
2. **Driver Comparison**: Visualizes the differences in accident frequency and severity between good and bad drivers
3. **Premium Calculation**: Demonstrates how insurance premiums are calculated

## Requirements

- Python 3.7+
- Packages: shiny, pandas, numpy, matplotlib, rsconnect-python

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the app locally:

```
shiny run app.py
```

## Deployment to shinyapps.io

1. Create an account on [shinyapps.io](https://www.shinyapps.io)
2. Install rsconnect-python:
   ```
   pip install rsconnect-python
   ```
3. Configure your account:
   ```
   rsconnect add --name shinyapps --token YOUR_TOKEN --secret YOUR_SECRET
   ```
4. Deploy the app:
   ```
   rsconnect deploy shiny . --name shinyapps --title InsuranceFundamentals
   ```

## Project Structure

- `app.py`: Main Shiny application file
- `modules/`: Directory containing the demonstration modules
  - `risk_pooling.py`: Risk Pooling demonstration
  - `driver_comparison.py`: Driver Comparison demonstration
  - `premium_calculation.py`: Premium Calculation demonstration
- `requirements.txt`: List of Python dependencies