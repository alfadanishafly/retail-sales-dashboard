import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import streamlit as st
import logging
from typing import Optional
from config import (
    DATA_START_DATE, DATA_END_DAYS, NUM_ROWS_DEFAULT,
    CATEGORIES, REGIONS, STORES, PRODUCTS, CUSTOMER_SEGMENTS,
    MIN_PRICE, MAX_PRICE, MIN_QUANTITY, MAX_QUANTITY,
    MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN, CACHE_TTL_SECONDS
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()

@st.cache_data(ttl=CACHE_TTL_SECONDS)
def load_data(n_rows: int = NUM_ROWS_DEFAULT) -> pd.DataFrame:
    """
    Generate synthetic retail transaction data.
    
    Args:
        n_rows: Number of rows to generate (default: 5000)
        
    Returns:
        DataFrame with synthetic retail transactions
    """
    logger.info(f"Generating {n_rows} rows of synthetic data")
    data = []
    
    try:
        for _ in range(n_rows):
            date = DATA_START_DATE + timedelta(days=random.randint(0, DATA_END_DAYS))
            qty = random.randint(MIN_QUANTITY, MAX_QUANTITY)
            price = random.uniform(MIN_PRICE, MAX_PRICE)
            product = random.choice(PRODUCTS)

            data.append({
                'Transaction_ID': fake.uuid4(),
                'Date': date,
                'Category': random.choice(CATEGORIES),
                'Region': random.choice(REGIONS),
                'Store': random.choice(STORES),
                'Product': product,
                'Quantity': qty,
                'Unit_Price': round(price, 2),
                'Total_Sales': round(qty * price, 2),
                'Profit': round((qty * price) * random.uniform(MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN), 2),
                'Customer_Segment': random.choice(CUSTOMER_SEGMENTS)
            })
        
        logger.info(f"Successfully generated {n_rows} rows")
        return pd.DataFrame(data)
    
    except Exception as e:
        logger.error(f"Error generating data: {str(e)}")
        raise