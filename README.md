# Retail Sales Analytics Dashboard

A modern, interactive retail sales dashboard built with Streamlit that provides comprehensive analytics and visualization for retail business data.

## 📋 Overview

This application generates synthetic retail sales data and presents it through an interactive dashboard with filtering capabilities, KPI metrics, and various visualizations. Users can filter data by date range, category, region, and store, then export the filtered results to Excel.

## ✨ Features

### Dashboard Analytics
- **KPI Metrics**: Total Revenue, Total Profit (with margin %), Items Sold, Average Order Value
- **Sales Trend Over Time**: Monthly revenue line chart with pastel color scheme
- **Revenue by Category**: Bar chart showing category performance
- **Sales by Region**: Pie chart displaying regional distribution
- **Customer Segment Breakdown**: Bar chart by customer type (New, Returning, VIP)
- **Revenue Performance by Store**: Horizontal bar chart ranking all stores

### Advanced Features
1. **Store Performance Ranking**: Interactive ranking from lowest to highest revenue
2. **Top 5 & Bottom 5 Products**: Identify best and worst selling products
3. **Excel Export**: Download filtered data with formatted sheets including:
   - Filtered raw data
   - Store summary with aggregated metrics

### Filtering Capabilities
- Date range selector (start and end date)
- Multi-select filters for Category, Region, and Store
- "Empty means all" logic - leaving filters empty includes all data

## 🏗️ Architecture

```
retail-sales-dashboard/
├── app.py                  # Main Streamlit application
├── data_generator.py       # Synthetic data generation module
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd retail-sales-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## 📦 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **faker**: Synthetic data generation
- **xlsxwriter**: Excel file writing for export functionality

## 🎨 Design Features

- **Color Scheme**: Pastel colors for professional, easy-on-the-eyes visuals
- **Layout**: Wide layout with organized sidebar filters
- **Responsive**: Charts automatically resize to container width
- **User Feedback**: Warning message when filters return no data

## 📊 Data Structure

The generated dataset includes the following columns:
- `Transaction_ID`: Unique identifier (UUID)
- `Date`: Transaction date (2025-2026 range)
- `Category`: Product category (5 categories)
- `Region`: Geographic region (5 Indonesian cities)
- `Store`: Store name (10 unique stores)
- `Product`: Specific product name (10 tech products)
- `Quantity`: Number of items purchased
- `Unit_Price`: Price per unit ($50-$2000)
- `Total_Sales`: Total transaction value
- `Profit`: Calculated profit (10-30% margin)
- `Customer_Segment`: Customer type (New, Returning, VIP)

## 🔧 Configuration

Default settings:
- **Data Size**: 5,000 rows (configurable in `load_data()`)
- **Date Range**: January 1, 2025 + 365 days
- **Cache**: Data loading is cached for performance

## 📝 Usage Tips

1. **Filtering**: Start with broad filters, then narrow down
2. **Export**: Use the Excel export to save filtered reports
3. **Analysis**: Compare top/bottom products to identify trends
4. **Performance**: Cached data ensures fast filter updates

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👥 Author

Alfa Dani Shafly Pratama

---

*Built with ❤️ using Streamlit*

p.s. see our example here https://retail-sales-dashboard-project.streamlit.app/
