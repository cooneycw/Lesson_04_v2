# Insurance Fundamentals - Shiny App

This is a Shiny for Python application demonstrating key insurance concepts through interactive visualizations, featuring Drake and Kendrick as example drivers.

## Features

The app includes three interactive modules:

1. **Risk Pooling**: Shows how insurance distributes risk across many policyholders
   - Adjust accident probability and number of policyholders
   - Visualize individual outcomes vs. pooled insurance results
   - See how the law of large numbers makes insurance pools more predictable

2. **Driver Comparison**: Visualizes the differences in accident frequency and severity between good and bad drivers
   - Use the stylish slider toggle to select either Drake or Kendrick as the "good driver"
   - Adjust frequency and severity parameters for both driver types
   - See how risk profiles cluster in a visual representation
   - Compare the expected losses between driver types

3. **Premium Calculation**: Demonstrates how insurance premiums are calculated
   - Uses data from the Driver Comparison module
   - Shows side-by-side comparison of Drake vs. Kendrick premiums
   - Visualizes the breakdown of premium components
   - Explains the formula for calculating insurance premiums

## Interactive Features

- **Drake vs. Kendrick Slider Toggle**: Visually appealing slider that switches between Drake (blue) and Kendrick (purple)
- **Dynamic Labels**: UI labels update based on your driver selection
- **Real-time Calculations**: See how changes in parameters affect outcomes
- **Re-simulate Button**: Generate new random data while keeping parameters the same
- **Visual Artist Integration**: See images of Drake and Kendrick in the premium comparison charts
- **Side-by-Side Comparison**: Equal-scaled charts for fair visual comparison of premiums

## Requirements

- Python 3.7+
- Packages: shiny, pandas, numpy, matplotlib, scipy, rsconnect-python

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure to place the following files in the modules directory:
   - drake.jpeg
   - kendrick.jpeg 

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
  - `drake.jpeg`: Image of Drake for visualizations
  - `kendrick.jpeg`: Image of Kendrick for visualizations
- `requirements.txt`: List of Python dependencies

## UI Features

- **Colorful Toggle Switch**: The Drake/Kendrick selector uses a stylish slider toggle with blue for Drake and purple for Kendrick
- **Responsive Design**: All components scale appropriately on different screen sizes
- **Clear Visual Hierarchy**: Important information is highlighted and properly organized
- **Interactive Elements**: Tooltips and dynamic labels enhance the user experience