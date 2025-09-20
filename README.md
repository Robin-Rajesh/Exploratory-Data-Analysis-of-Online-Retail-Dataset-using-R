# Online Retail Analytics Dashboard

A comprehensive web-based dashboard for analyzing online retail data using R and Python.

## Features

- **Real-time Analytics**: Run R analysis scripts and display results in a modern web interface
- **Interactive Charts**: Visualize monthly revenue trends, top products, and country performance
- **Key Metrics**: Display important KPIs like customer count, repeat customer percentage, and average order value
- **Responsive Design**: Modern, mobile-friendly interface with Bootstrap styling
- **API Endpoints**: RESTful API for data access and refresh functionality

## Quick Start

### Prerequisites

- R (with tidyverse, lubridate, readxl packages)
- Python 3 (with Flask, pandas, numpy)
- Modern web browser

### Running the Dashboard

1. **Start the Dashboard Server**:
   ```bash
   python3 dashboard_server.py
   ```

2. **Open Your Browser**:
   Navigate to `http://localhost:5000`

3. **View the Analysis**:
   The dashboard will automatically load with the latest analysis results

## Files Structure

```
robin/
├── pa.r                    # R analysis script
├── Online Retail (1).xlsx  # Source data file
├── index.html             # Web dashboard interface
├── dashboard_server.py    # Python Flask server
└── README.md             # This file
```

## Analysis Components

### Key Metrics
- **Total Customers**: 4,338 unique customers
- **Repeat Customers**: 65.6% customer retention rate
- **Average Order Value**: $480 per order
- **Average Quantity**: 13.1 items per order

### Visualizations
- **Monthly Revenue Trend**: Line chart showing revenue growth over time
- **Top Products by Quantity**: Bar chart of best-selling products
- **Revenue by Country**: Table showing geographic performance
- **Top Products by Revenue**: Table showing highest revenue generators

### Insights
- Singapore has the highest average order value ($3,040)
- United Kingdom dominates total revenue ($7.3M)
- Strong customer loyalty with 65.6% repeat customers

## API Endpoints

- `GET /` - Main dashboard interface
- `GET /api/data` - Get current analysis data
- `GET /api/refresh` - Refresh analysis data from R script

## Technical Details

### R Analysis (`pa.r`)
- Data cleaning and preprocessing
- Summary statistics calculation
- Product and customer analysis
- Revenue trend analysis
- Geographic performance metrics

### Web Interface (`index.html`)
- Modern responsive design
- Interactive charts using Chart.js
- Bootstrap styling
- Real-time data updates

### Server (`dashboard_server.py`)
- Flask web server
- R script execution
- Data parsing and API endpoints
- Error handling and fallback data

## Customization

To modify the analysis:
1. Edit `pa.r` to change the R analysis logic
2. Update `dashboard_server.py` to modify data parsing
3. Modify `index.html` to change the UI components

## Troubleshooting

- **R not found**: Install R using `brew install r`
- **Packages missing**: Install R packages with `install.packages(c('tidyverse', 'lubridate', 'readxl'))`
- **Port in use**: Change port in `dashboard_server.py` if 5000 is occupied
- **Data not loading**: Check that `Online Retail (1).xlsx` exists in the directory

## Future Enhancements

- Real-time data updates
- Export functionality for charts and tables
- Advanced filtering and drill-down capabilities
- User authentication and multi-tenant support
- Integration with live data sources
