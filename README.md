# Skyline Sales Dashboard

An interactive dashboard built with Streamlit, designed to help Skyline Gadgets analyze historical sales performance across products, categories, and time periods.

## Features

- KPI overview: Total Revenue, Units Sold, Transactions
- Monthly revenue trend
- Top 5 revenue-generating products
- Category revenue breakdown (pie chart)
- Revenue heatmap (Category × Month)
- Pareto analysis (80/20 rule)
- Inline filters for category, product, and month
- Missing data summary and raw data viewer

## Project Structure

skyline_dashboard_deploy/<br>
├── tableau_style_dashboard.py # Streamlit app <br>
└── May Cohort Sales_data.xlsx # Sales data (Excel) <br>


## How to Run Locally

1. Clone the repository or download the ZIP  
2. Install the required packages:
   ```bash
   pip install streamlit pandas plotly openpyxl
   
## Run the Streamlit app:
streamlit run tableau_style_dashboard.py

## The dashboard will open in your browser at:
http://localhost:8501

- **Streamlit**  
  - Used to build and deploy the interactive dashboard interface
