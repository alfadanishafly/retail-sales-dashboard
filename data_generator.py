import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import streamlit as st

fake = Faker()

@st.cache_data # <-- Ini magic-nya biar gak lemot
def load_data(n_rows=5000):
    data = []
    start_date = datetime(2025, 1, 1) # Set tahun ke 2025/2026 biar fresh
    
    categories = ['Electronics', 'Fashion', 'Home & Living', 'F&B', 'Beauty']
    regions = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Bali']
    
    # Tambahin 10 Nama Store (Bisa lu ganti sesuai selera)
    stores = [
        'Grand Retail Plaza', 'Metro City Mall', 'Pusat Grosir Utama', 
        'Retail Hub Selatan', 'Pasar Modern Jaya', 'Mega Store Indah', 
        'Central Shopping Center', 'East Point Retail', 'West Mall Outlet', 
        'North Star Department Store'
    ]

        # Tambahin list produk ini di bawah list categories/regions
    products = [
        'Laptop Pro', 'Wireless Mouse', 'Mechanical Keyboard', '4K Monitor', 
        'Noise Cancelling Headset', 'Smartwatch', 'Bluetooth Speaker', 
        'USB-C Hub', 'Webcam HD', 'Gaming Chair'
    ]

    for _ in range(n_rows):
        date = start_date + timedelta(days=random.randint(0, 365))
        qty = random.randint(1, 10)
        price = random.uniform(50, 2000)
        product = random.choice(products)

        data.append({
            'Transaction_ID': fake.uuid4(),
            'Date': date,
            'Category': random.choice(categories),
            'Region': random.choice(regions),
            'Store': random.choice(stores),
            'Product': product,
            'Quantity': qty,
            'Unit_Price': round(price, 2),
            'Total_Sales': round(qty * price, 2),
            'Profit': round((qty * price) * random.uniform(0.1, 0.3), 2), # Profit margin 10-30%
            'Customer_Segment': random.choice(['New', 'Returning', 'VIP'])
        })
        
    return pd.DataFrame(data)