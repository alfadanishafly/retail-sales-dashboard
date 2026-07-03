"""
Configuration settings for Retail Sales Analytics Dashboard
Centralized configuration to avoid hardcoded values
"""
from datetime import datetime, timedelta

# Data Generation Configuration
DATA_START_DATE = datetime(2025, 1, 1)
DATA_END_DAYS = 365
NUM_ROWS_DEFAULT = 5000

# Business Categories
CATEGORIES = ['Electronics', 'Fashion', 'Home & Living', 'F&B', 'Beauty']

# Geographic Regions
REGIONS = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Bali']

# Store Names
STORES = [
    'Grand Retail Plaza', 'Metro City Mall', 'Pusat Grosir Utama', 
    'Retail Hub Selatan', 'Pasar Modern Jaya', 'Mega Store Indah', 
    'Central Shopping Center', 'East Point Retail', 'West Mall Outlet', 
    'North Star Department Store'
]

# Product List
PRODUCTS = [
    'Laptop Pro', 'Wireless Mouse', 'Mechanical Keyboard', '4K Monitor', 
    'Noise Cancelling Headset', 'Smartwatch', 'Bluetooth Speaker', 
    'USB-C Hub', 'Webcam HD', 'Gaming Chair'
]

# Customer Segments
CUSTOMER_SEGMENTS = ['New', 'Returning', 'VIP']

# Price Range
MIN_PRICE = 50.0
MAX_PRICE = 2000.0

# Quantity Range
MIN_QUANTITY = 1
MAX_QUANTITY = 10

# Profit Margin Range
MIN_PROFIT_MARGIN = 0.1  # 10%
MAX_PROFIT_MARGIN = 0.3  # 30%

# Security & Performance Limits
MAX_DATE_RANGE_DAYS = 730  # Maximum 2 years
MAX_EXPORT_ROWS = 10000    # Maximum rows for Excel export
EXPORT_COOLDOWN_SECONDS = 30  # Minimum time between exports
CACHE_TTL_SECONDS = 3600   # Cache expires after 1 hour

# UI Configuration
PAGE_TITLE = "Retail Sales Dashboard"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Color Schemes
COLOR_PASTEL_BLUE = '#AEC6CF'
COLOR_PASTEL_RED = '#FFB7B2'
BG_COLOR = '#FDFBF7'
FONT_COLOR = '#4A4A4A'
