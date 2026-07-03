import streamlit as st
import pandas as pd
import plotly.express as px
from data_generator import load_data
import plotly.express as px
import io

# --- Page Config ---
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- Load Data ---
df = load_data()

# --- Sidebar Filters (Tanpa Default, Biar User Bebas Pilih) ---
st.sidebar.header("🔍 Filter Dashboard")

# Filter Tanggal
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

# Filter Kategori, Region, Store (Dibiarkan kosong by default)
categories = st.sidebar.multiselect("Category", df['Category'].unique())
regions = st.sidebar.multiselect("Region", df['Region'].unique())
stores = st.sidebar.multiselect("Store", df['Store'].unique())

# --- LOGIKA "EMPTY MEANS ALL" ---
# Cek filter satu-satu. Kalau kosong (user gak pilih apa-apa), otomatis diisi SEMUA data unik.
cat_filter = categories if categories else df['Category'].unique()
reg_filter = regions if regions else df['Region'].unique()
store_filter = stores if stores else df['Store'].unique()

# --- Apply Filters ---
mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date) & \
       (df['Category'].isin(cat_filter)) & (df['Region'].isin(reg_filter)) & \
       (df['Store'].isin(store_filter))

filtered_df = df[mask]

# Safety net: Kalau data beneran kosong (misal filter tanggal yang gak ada datanya)
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang cocok dengan filter yang dipilih. Silakan ubah filter Anda.")
    st.stop()

# --- Main Dashboard ---
st.title("Retail Sales Analytics Dashboard")
st.markdown("---")

# KPI Metrics (Kolom atas)
col1, col2, col3, col4 = st.columns(4)
total_sales = filtered_df['Total_Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_qty = filtered_df['Quantity'].sum()
avg_order = filtered_df['Total_Sales'].mean()

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}", delta=f"{(total_profit/total_sales*100):.1f}% Margin")
col3.metric("Items Sold", f"{total_qty:,}")
col4.metric("Avg Order Value", f"${avg_order:,.2f}")

st.markdown("---")

# --- Charts (Kolom bawah) ---
chart_col1, chart_col2 = st.columns(2)

# 1. Sales Trend (Line Chart) - Pake Pastel Blue
with chart_col1:
    st.subheader("Sales Trend Over Time")
    df_monthly = filtered_df.set_index('Date').resample('ME')['Total_Sales'].sum().reset_index()
    fig_line = px.line(df_monthly, x='Date', y='Total_Sales', title='Monthly Revenue')
    # Ubah warna garis jadi pastel
    fig_line.update_traces(line=dict(color='#AEC6CF', width=3))
    fig_line.update_layout(plot_bgcolor='white', paper_bgcolor='#FDFBF7', font=dict(color='#4A4A4A'))
    st.plotly_chart(fig_line, use_container_width=True)

# 2. Sales by Category (Bar Chart) - Pake Palette Pastel
with chart_col2:
    st.subheader("Revenue by Category")
    df_cat = filtered_df.groupby('Category')['Total_Sales'].sum().reset_index()
    # Tambahin color_discrete_sequence=px.colors.qualitative.Pastel
    fig_bar = px.bar(df_cat, x='Category', y='Total_Sales', title='Category Performance',
                     color='Category', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_bar.update_layout(plot_bgcolor='white', paper_bgcolor='#FDFBF7', font=dict(color='#4A4A4A'))
    st.plotly_chart(fig_bar, use_container_width=True)

# 3. Region Distribution (Pie Chart)
chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    st.subheader("Sales by Region")
    df_region = filtered_df.groupby('Region')['Total_Sales'].sum().reset_index()
    fig_pie = px.pie(df_region, values='Total_Sales', names='Region', hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel2) # Pake Pastel2 biar beda dikit
    fig_pie.update_layout(paper_bgcolor='#FDFBF7', font=dict(color='#4A4A4A'))
    st.plotly_chart(fig_pie, use_container_width=True)

# 4. Customer Segment (Bar Chart)
with chart_col4:
    st.subheader("Customer Segment Breakdown")
    df_seg = filtered_df.groupby('Customer_Segment')['Total_Sales'].sum().reset_index()
    fig_seg = px.bar(df_seg, x='Customer_Segment', y='Total_Sales', color='Customer_Segment',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_seg.update_layout(plot_bgcolor='white', paper_bgcolor='#FDFBF7', font=dict(color='#4A4A4A'))
    st.plotly_chart(fig_seg, use_container_width=True)

# 5. Performance per Store (Horizontal Bar Chart - Biar nama store kebaca semua)
st.subheader("Revenue Performance by Store")
df_store = filtered_df.groupby('Store')['Total_Sales'].sum().reset_index().sort_values(by='Total_Sales', ascending=True)
fig_store = px.bar(df_store, x='Total_Sales', y='Store', orientation='h', 
                   color='Total_Sales', color_continuous_scale='mint') # Ganti 'Pastel' jadi 'mint'
fig_store.update_layout(plot_bgcolor='white', paper_bgcolor='#FDFBF7', font=dict(color='#4A4A4A'))
st.plotly_chart(fig_store, use_container_width=True)


st.markdown("---")

# ==========================================
# FITUR 1: STORE PERFORMANCE RANKING
# ==========================================
st.subheader(" Store Performance Ranking")
st.caption("Ranking total revenue per store dari yang terendah ke tertinggi")

# Groupby dan sort
df_store_rank = filtered_df.groupby('Store')['Total_Sales'].sum().sort_values(ascending=True)

fig_store_rank = px.bar(
    df_store_rank, 
    x='Total_Sales', 
    y=df_store_rank.index, 
    orientation='h',
    color='Total_Sales', 
    color_continuous_scale='mint',
    title='Total Revenue by Store'
)
# Hilangkan legend biar lebih clean
fig_store_rank.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='#FDFBF7')
st.plotly_chart(fig_store_rank, use_container_width=True)


# ==========================================
# FITUR 2: TOP 5 & BOTTOM 5 PRODUCTS
# ==========================================
st.subheader("Top 5 & Bottom 5 Best Selling Products")
st.caption("Produk dengan revenue tertinggi dan terendah berdasarkan filter saat ini")

col_top, col_bot = st.columns(2)

# Hitung total sales per product
df_prod = filtered_df.groupby('Product')['Total_Sales'].sum()

with col_top:
    st.markdown("#### Top 5 Products")
    top_5 = df_prod.nlargest(5)
    fig_top = px.bar(top_5, x=top_5.values, y=top_5.index, orientation='h', color_discrete_sequence=['#AEC6CF'])
    fig_top.update_layout(showlegend=False, xaxis_title="Revenue", yaxis_title="Product", plot_bgcolor='white')
    st.plotly_chart(fig_top, use_container_width=True)

with col_bot:
    st.markdown("#### Bottom 5 Products")
    bot_5 = df_prod.nsmallest(5)
    fig_bot = px.bar(bot_5, x=bot_5.values, y=bot_5.index, orientation='h', color_discrete_sequence=['#FFB7B2']) # Pastel Red
    fig_bot.update_layout(showlegend=False, xaxis_title="Revenue", yaxis_title="Product", plot_bgcolor='white')
    st.plotly_chart(fig_bot, use_container_width=True)


# ==========================================
# FITUR 3: EXPORT TO EXCEL (THE KILLER FEATURE)
# ==========================================
st.markdown("---")
st.subheader("Download Filtered Report")
st.caption("Download data yang sudah di-filter ke dalam format Excel yang rapi.")

# 1. Siapkan buffer di memory (biar gak numpuk file sampah)
output = io.BytesIO()

# 2. DEFINISI df_store_summary (Ini yang tadi kelewatan!)
df_store_summary = filtered_df.groupby('Store').agg(
    Total_Revenue=('Total_Sales', 'sum'),
    Total_Items_Sold=('Quantity', 'sum'),
    Total_Transactions=('Transaction_ID', 'count')
).reset_index()

# 3. Tulis ke Excel pake xlsxwriter
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    
    # --- Format Header (Bikin tebal & warna pastel) ---
    workbook = writer.book
    header_format = workbook.add_format({
        'bold': True, 
        'bg_color': '#AEC6CF', # Pastel Blue
        'font_color': 'white',
        'border': 1
    })

    # Sheet 1: Data Mentah yang sudah di-filter
    filtered_df.to_excel(writer, sheet_name='Filtered Data', index=False)
    worksheet1 = writer.sheets['Filtered Data']
    for col_num, value in enumerate(filtered_df.columns.values):
        worksheet1.write(0, col_num, value, header_format)
    for i, col in enumerate(filtered_df.columns):
        column_len = max(filtered_df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet1.set_column(i, i, column_len)

    # Sheet 2: Summary Store
    df_store_summary.to_excel(writer, sheet_name='Store Summary', index=False)
    worksheet2 = writer.sheets['Store Summary']
    for col_num, value in enumerate(df_store_summary.columns.values):
        worksheet2.write(0, col_num, value, header_format)
    for i, col in enumerate(df_store_summary.columns):
        column_len = max(df_store_summary[col].astype(str).map(len).max(), len(col)) + 2
        worksheet2.set_column(i, i, column_len)

# 4. Tombol Download
st.download_button(
    label="️ Download Excel Report",
    data=output.getvalue(),
    file_name="Retail_Dashboard_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
