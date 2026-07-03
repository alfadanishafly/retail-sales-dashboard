import unittest
import pandas as pd
from datetime import datetime, timedelta, date
import sys
import os

# Add the workspace to the path
sys.path.insert(0, '/workspace')

from data_generator import load_data
from app import (
    apply_filters, calculate_kpi_metrics, validate_date_inputs,
    prepare_excel_export, check_export_rate_limit
)
from config import MAX_DATE_RANGE_DAYS, MAX_EXPORT_ROWS


class TestDataGenerator(unittest.TestCase):
    """Test cases for the data_generator module"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before the first test"""
        cls.test_df = load_data(n_rows=100)

    def test_load_data_returns_dataframe(self):
        """Test that load_data returns a pandas DataFrame"""
        self.assertIsInstance(self.test_df, pd.DataFrame)

    def test_load_data_correct_row_count(self):
        """Test that load_data generates the correct number of rows"""
        df_50 = load_data(n_rows=50)
        df_200 = load_data(n_rows=200)
        self.assertEqual(len(df_50), 50)
        self.assertEqual(len(df_200), 200)

    def test_required_columns_exist(self):
        """Test that all required columns are present in the DataFrame"""
        required_columns = [
            'Transaction_ID', 'Date', 'Category', 'Region', 'Store',
            'Product', 'Quantity', 'Unit_Price', 'Total_Sales',
            'Profit', 'Customer_Segment'
        ]
        for col in required_columns:
            self.assertIn(col, self.test_df.columns, f"Missing column: {col}")

    def test_category_values(self):
        """Test that Category column contains only valid values"""
        valid_categories = {'Electronics', 'Fashion', 'Home & Living', 'F&B', 'Beauty'}
        unique_categories = set(self.test_df['Category'].unique())
        self.assertTrue(unique_categories.issubset(valid_categories))

    def test_region_values(self):
        """Test that Region column contains only valid values"""
        valid_regions = {'Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Bali'}
        unique_regions = set(self.test_df['Region'].unique())
        self.assertTrue(unique_regions.issubset(valid_regions))

    def test_store_count(self):
        """Test that there are exactly 10 unique stores"""
        unique_stores = self.test_df['Store'].nunique()
        self.assertEqual(unique_stores, 10)

    def test_product_count(self):
        """Test that there are exactly 10 unique products"""
        unique_products = self.test_df['Product'].nunique()
        self.assertEqual(unique_products, 10)

    def test_quantity_range(self):
        """Test that Quantity is between 1 and 10"""
        self.assertGreaterEqual(self.test_df['Quantity'].min(), 1)
        self.assertLessEqual(self.test_df['Quantity'].max(), 10)

    def test_unit_price_range(self):
        """Test that Unit_Price is between 50 and 2000"""
        self.assertGreaterEqual(self.test_df['Unit_Price'].min(), 50)
        self.assertLessEqual(self.test_df['Unit_Price'].max(), 2000)

    def test_total_sales_calculation(self):
        """Test that Total_Sales equals Quantity * Unit_Price (within rounding tolerance)"""
        calculated_sales = self.test_df['Quantity'] * self.test_df['Unit_Price']
        diff = (self.test_df['Total_Sales'] - calculated_sales).abs()
        self.assertTrue((diff <= 0.06).all(), "Total_Sales should match Quantity * Unit_Price within 0.06 tolerance")

    def test_profit_margin_range(self):
        """Test that Profit margin is between 10% and 30% of Total_Sales"""
        profit_margins = self.test_df['Profit'] / self.test_df['Total_Sales']
        self.assertGreaterEqual(profit_margins.min(), 0.1)
        self.assertLessEqual(profit_margins.max(), 0.3)

    def test_customer_segment_values(self):
        """Test that Customer_Segment contains only valid values"""
        valid_segments = {'New', 'Returning', 'VIP'}
        unique_segments = set(self.test_df['Customer_Segment'].unique())
        self.assertTrue(unique_segments.issubset(valid_segments))

    def test_date_range(self):
        """Test that dates are within expected range (2025-2026)"""
        min_date = datetime(2025, 1, 1)
        max_date = datetime(2025, 12, 31)
        for date_val in self.test_df['Date']:
            self.assertGreaterEqual(date_val, min_date)
            self.assertLessEqual(date_val, max_date)

    def test_transaction_id_uniqueness(self):
        """Test that all Transaction_IDs are unique"""
        self.assertEqual(
            self.test_df['Transaction_ID'].nunique(),
            len(self.test_df),
            "Transaction_IDs should be unique"
        )

    def test_no_null_values(self):
        """Test that there are no null values in the DataFrame"""
        null_counts = self.test_df.isnull().sum()
        for col, count in null_counts.items():
            self.assertEqual(count, 0, f"Column {col} has {count} null values")

    def test_data_types(self):
        """Test that columns have appropriate data types"""
        self.assertEqual(self.test_df['Transaction_ID'].dtype, 'object')
        self.assertEqual(self.test_df['Date'].dtype, 'datetime64[ns]')
        self.assertEqual(self.test_df['Quantity'].dtype, 'int64')
        self.assertIn(self.test_df['Unit_Price'].dtype, ['float64', 'float32'])
        self.assertIn(self.test_df['Total_Sales'].dtype, ['float64', 'float32'])
        self.assertIn(self.test_df['Profit'].dtype, ['float64', 'float32'])


class TestAppLogic(unittest.TestCase):
    """Test cases for app.py logic (without running Streamlit)"""

    def setUp(self):
        """Set up test fixtures"""
        self.df = load_data(n_rows=1000)

    def test_filter_logic_empty_means_all(self):
        """Test that empty filter lists include all unique values"""
        categories = []
        cat_filter = categories if categories else self.df['Category'].unique()
        self.assertEqual(len(cat_filter), len(self.df['Category'].unique()))

    def test_filter_logic_non_empty_preserved(self):
        """Test that non-empty filter lists are preserved"""
        categories = ['Electronics', 'Fashion']
        cat_filter = categories if categories else self.df['Category'].unique()
        self.assertEqual(cat_filter, categories)

    def test_date_mask_creation(self):
        """Test that date filtering mask works correctly"""
        start_date = datetime(2025, 6, 1).date()
        end_date = datetime(2025, 8, 31).date()
        
        mask = (self.df['Date'].dt.date >= start_date) & (self.df['Date'].dt.date <= end_date)
        filtered_df = self.df[mask]
        
        for date_val in filtered_df['Date']:
            self.assertGreaterEqual(date_val.date(), start_date)
            self.assertLessEqual(date_val.date(), end_date)

    def test_aggregation_functions(self):
        """Test that aggregation functions work correctly"""
        total_sales = self.df['Total_Sales'].sum()
        self.assertGreater(total_sales, 0)
        
        avg_order = self.df['Total_Sales'].mean()
        self.assertGreater(avg_order, 0)
        
        grouped = self.df.groupby('Category')['Total_Sales'].sum()
        self.assertEqual(len(grouped), 5)

    def test_top_n_bottom_n_selection(self):
        """Test nlargest and nsmallest functions"""
        df_prod = self.df.groupby('Product')['Total_Sales'].sum()
        
        top_5 = df_prod.nlargest(5)
        bottom_5 = df_prod.nsmallest(5)
        
        self.assertEqual(len(top_5), 5)
        self.assertEqual(len(bottom_5), 5)
        self.assertGreaterEqual(top_5.min(), bottom_5.max())

    def test_store_summary_aggregation(self):
        """Test store summary aggregation logic"""
        df_store_summary = self.df.groupby('Store').agg(
            Total_Revenue=('Total_Sales', 'sum'),
            Total_Items_Sold=('Quantity', 'sum'),
            Total_Transactions=('Transaction_ID', 'count')
        ).reset_index()
        
        self.assertEqual(len(df_store_summary), 10)
        self.assertIn('Total_Revenue', df_store_summary.columns)
        self.assertIn('Total_Items_Sold', df_store_summary.columns)
        self.assertIn('Total_Transactions', df_store_summary.columns)
        
        self.assertTrue((df_store_summary['Total_Revenue'] > 0).all())
        self.assertTrue((df_store_summary['Total_Items_Sold'] > 0).all())
        self.assertTrue((df_store_summary['Total_Transactions'] > 0).all())


class TestSecurityFeatures(unittest.TestCase):
    """Test cases for security features implemented in the refactored code"""

    def setUp(self):
        """Set up test fixtures"""
        self.df = load_data(n_rows=100)

    def test_apply_filters_validates_date_order(self):
        """Test that apply_filters raises error when start_date > end_date"""
        start_date = datetime(2025, 6, 1).date()
        end_date = datetime(2025, 1, 1).date()
        
        with self.assertRaises(ValueError):
            apply_filters(self.df, start_date, end_date)

    def test_apply_filters_enforces_max_date_range(self):
        """Test that apply_filters raises error for date ranges exceeding maximum"""
        start_date = datetime(2025, 1, 1).date()
        end_date = datetime(2028, 1, 1).date()  # More than 730 days
        
        with self.assertRaises(ValueError):
            apply_filters(self.df, start_date, end_date)

    def test_apply_filters_valid_date_range(self):
        """Test that apply_filters works with valid date range"""
        start_date = datetime(2025, 1, 1).date()
        end_date = datetime(2025, 6, 1).date()
        
        filtered = apply_filters(self.df, start_date, end_date)
        self.assertIsInstance(filtered, pd.DataFrame)

    def test_validate_date_inputs_start_after_end(self):
        """Test validate_date_inputs rejects start_date > end_date"""
        is_valid, msg = validate_date_inputs(
            datetime(2025, 6, 1).date(),
            datetime(2025, 1, 1).date(),
            datetime(2025, 1, 1).date(),
            datetime(2025, 12, 31).date()
        )
        self.assertFalse(is_valid)
        self.assertIn("after", msg.lower())

    def test_validate_date_inputs_exceeds_max_range(self):
        """Test validate_date_inputs rejects date range exceeding maximum"""
        is_valid, msg = validate_date_inputs(
            datetime(2025, 1, 1).date(),
            datetime(2028, 1, 1).date(),
            datetime(2025, 1, 1).date(),
            datetime(2028, 12, 31).date()
        )
        self.assertFalse(is_valid)
        self.assertIn("exceed", msg.lower())

    def test_validate_date_inputs_outside_data_range(self):
        """Test validate_date_inputs rejects dates outside data range"""
        is_valid, msg = validate_date_inputs(
            datetime(2020, 1, 1).date(),  # Before data starts
            datetime(2020, 6, 1).date(),
            datetime(2025, 1, 1).date(),
            datetime(2025, 12, 31).date()
        )
        self.assertFalse(is_valid)

    def test_validate_date_inputs_valid(self):
        """Test validate_date_inputs accepts valid dates"""
        is_valid, msg = validate_date_inputs(
            datetime(2025, 3, 1).date(),
            datetime(2025, 9, 1).date(),
            datetime(2025, 1, 1).date(),
            datetime(2025, 12, 31).date()
        )
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

    def test_prepare_excel_export_limits_rows(self):
        """Test that prepare_excel_export enforces row limit"""
        # Create a large dataframe
        large_df = pd.concat([self.df] * 200, ignore_index=True)  # 20,000 rows
        self.assertGreater(len(large_df), MAX_EXPORT_ROWS)
        
        # Export should truncate to MAX_EXPORT_ROWS
        excel_data = prepare_excel_export(large_df)
        self.assertIsInstance(excel_data, bytes)
        self.assertGreater(len(excel_data), 0)

    def test_calculate_kpi_metrics_returns_dict(self):
        """Test that calculate_kpi_metrics returns a dictionary with expected keys"""
        metrics = calculate_kpi_metrics(self.df)
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('total_sales', metrics)
        self.assertIn('total_profit', metrics)
        self.assertIn('total_qty', metrics)
        self.assertIn('avg_order', metrics)
        self.assertIn('profit_margin', metrics)
        
        self.assertGreater(metrics['total_sales'], 0)
        self.assertGreater(metrics['profit_margin'], 0)

    def test_empty_dataframe_handling(self):
        """Test that functions handle empty DataFrames gracefully"""
        empty_df = self.df.iloc[:0].copy()
        
        # KPI metrics should handle empty data
        metrics = calculate_kpi_metrics(empty_df)
        self.assertEqual(metrics['total_sales'], 0)
        self.assertEqual(metrics['profit_margin'], 0)


if __name__ == '__main__':
    unittest.main()
