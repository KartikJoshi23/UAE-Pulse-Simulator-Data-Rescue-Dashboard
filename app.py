# ============================================================================
# UAE Pulse Simulator + Data Rescue Dashboard
# Main Streamlit Application
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Import custom modules
from modules.cleaner import DataCleaner
from modules.simulator import Simulator
from modules.utils import (
    CONFIG, SIMULATOR_CONFIG, CHART_THEME, 
    style_plotly_chart, load_sample_data, get_data_summary
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="UAE Pulse Simulator",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - DARK THEME WITH PROFESSIONAL COLORS
# ============================================================================

st.markdown("""
<style>
    /* ===== MAIN BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #4a4a8a;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
    
    /* ===== HEADERS ===== */
    h1 {
        color: #a78bfa !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2 {
        color: #8b5cf6 !important;
    }
    
    h3 {
        color: #7c3aed !important;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(135deg, #1e1e3f 0%, #2d2d5a 100%);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #4a4a8a;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        margin: 10px 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        border-color: #8b5cf6;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #a78bfa;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-delta-positive {
        color: #10b981;
        font-size: 0.9rem;
    }
    
    .metric-delta-negative {
        color: #ef4444;
        font-size: 0.9rem;
    }
    
    /* ===== INFO CARDS ===== */
    .info-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #1e1e3f 100%);
        border-radius: 12px;
        padding: 15px 20px;
        border-left: 4px solid #3b82f6;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateX(5px);
        border-left-color: #8b5cf6;
    }
    
    /* ===== SUCCESS/WARNING/ERROR CARDS ===== */
    .success-card {
        background: linear-gradient(135deg, #064e3b 0%, #1e3a3a 100%);
        border-radius: 12px;
        padding: 15px 20px;
        border-left: 4px solid #10b981;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .success-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #78350f 0%, #3d2a1e 100%);
        border-radius: 12px;
        padding: 15px 20px;
        border-left: 4px solid #f59e0b;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .warning-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    .error-card {
        background: linear-gradient(135deg, #7f1d1d 0%, #3d1e1e 100%);
        border-radius: 12px;
        padding: 15px 20px;
        border-left: 4px solid #ef4444;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .error-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
    }
    
    /* ===== FEATURE CARDS ===== */
    .feature-card {
        background: linear-gradient(135deg, #1e1e3f 0%, #2d2d5a 100%);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #4a4a8a;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        margin: 10px 0;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(139, 92, 246, 0.3);
        border-color: #8b5cf6;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        color: #a78bfa;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        color: #9ca3af;
        font-size: 0.9rem;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        transform: translateY(-2px);
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1e1e3f;
        border-radius: 10px;
        color: #9ca3af;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%);
        color: white;
    }
    
    /* ===== DATAFRAME ===== */
    .dataframe {
        background-color: #1e1e3f !important;
        color: #e0e0e0 !important;
        border-radius: 10px;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1a 100%);
        padding: 20px;
        text-align: center;
        border-top: 1px solid #4a4a8a;
        color: #9ca3af;
        font-size: 0.9rem;
        margin-top: 50px;
        border-radius: 15px 15px 0 0;
    }
    
    .footer-names {
        color: #8b5cf6;
        font-weight: 600;
        font-size: 1rem;
        margin-top: 5px;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border-color: #4a4a8a;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background-color: #1e1e3f;
        color: #e0e0e0;
        border-radius: 10px;
    }
    
    /* ===== SLIDER ===== */
    .stSlider > div > div > div > div {
        background-color: #8b5cf6;
    }
    
    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background-color: #1e1e3f;
        color: #e0e0e0;
        border-color: #4a4a8a;
    }
    
    /* ===== NUMBER INPUT ===== */
    .stNumberInput > div > div > input {
        background-color: #1e1e3f;
        color: #e0e0e0;
        border-color: #4a4a8a;
    }
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS FOR UI
# ============================================================================

def create_metric_card(label, value, delta=None, delta_type="positive"):
    """Create a styled metric card with hover effect."""
    delta_html = ""
    if delta:
        delta_class = "metric-delta-positive" if delta_type == "positive" else "metric-delta-negative"
        delta_symbol = "↑" if delta_type == "positive" else "↓"
        delta_html = f'<div class="{delta_class}">{delta_symbol} {delta}</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def create_feature_card(icon, title, description):
    """Create a feature card with hover effect."""
    return f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """

def create_info_card(content):
    """Create an info card."""
    return f'<div class="info-card">{content}</div>'

def create_success_card(content):
    """Create a success card."""
    return f'<div class="success-card">✅ {content}</div>'

def create_warning_card(content):
    """Create a warning card."""
    return f'<div class="warning-card">⚠️ {content}</div>'

def create_error_card(content):
    """Create an error card."""
    return f'<div class="error-card">❌ {content}</div>'

def show_footer():
    """Display the footer with team names."""
    st.markdown("""
    <div class="footer">
        <div>🛒 UAE Pulse Simulator + Data Rescue Dashboard</div>
        <div style="margin-top: 5px; color: #6b7280;">Built with ❤️ by</div>
        <div class="footer-names">Kartik Joshi | Gagandeep Singh | Samuel Alex | Prem Kukreja</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if 'raw_products' not in st.session_state:
    st.session_state.raw_products = None
if 'raw_stores' not in st.session_state:
    st.session_state.raw_stores = None
if 'raw_sales' not in st.session_state:
    st.session_state.raw_sales = None
if 'raw_inventory' not in st.session_state:
    st.session_state.raw_inventory = None
if 'clean_products' not in st.session_state:
    st.session_state.clean_products = None
if 'clean_stores' not in st.session_state:
    st.session_state.clean_stores = None
if 'clean_sales' not in st.session_state:
    st.session_state.clean_sales = None
if 'clean_inventory' not in st.session_state:
    st.session_state.clean_inventory = None
if 'issues_df' not in st.session_state:
    st.session_state.issues_df = None
if 'is_cleaned' not in st.session_state:
    st.session_state.is_cleaned = False
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
  # ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    # Logo/Title
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #a78bfa; font-size: 1.8rem; margin-bottom: 5px;">🛒 UAE Pulse</h1>
        <p style="color: #9ca3af; font-size: 0.85rem;">Simulator + Data Rescue</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown('<p style="color: #8b5cf6; font-weight: 600; margin-bottom: 10px;">📍 NAVIGATION</p>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📂 Data", "🧹 Cleaner", "🎯 Simulator", "📊 Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Data Status
    st.markdown('<p style="color: #8b5cf6; font-weight: 600; margin-bottom: 10px;">📡 DATA STATUS</p>', unsafe_allow_html=True)
    
    data_loaded = st.session_state.data_loaded
    data_cleaned = st.session_state.is_cleaned
    
    status_color_loaded = "#10b981" if data_loaded else "#ef4444"
    status_color_cleaned = "#10b981" if data_cleaned else "#f59e0b" if data_loaded else "#ef4444"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 8px 0;">
        <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color_loaded}; margin-right: 10px;"></div>
        <span style="color: #e0e0e0;">Data Loaded</span>
    </div>
    <div style="display: flex; align-items: center; margin: 8px 0;">
        <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color_cleaned}; margin-right: 10px;"></div>
        <span style="color: #e0e0e0;">Data Cleaned</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    if st.session_state.data_loaded:
        st.markdown("---")
        st.markdown('<p style="color: #8b5cf6; font-weight: 600; margin-bottom: 10px;">📈 QUICK STATS</p>', unsafe_allow_html=True)
        
        sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
        if sales_df is not None:
            st.markdown(f"""
            <div style="background: #1e1e3f; padding: 10px; border-radius: 8px; margin: 5px 0;">
                <span style="color: #9ca3af;">Orders:</span> 
                <span style="color: #a78bfa; font-weight: bold;">{len(sales_df):,}</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PAGE: HOME
# ============================================================================

def show_home_page():
    """Display the home page."""
    
    # Header
    st.markdown("""
    <h1 style="text-align: center; margin-bottom: 0;">🛒 UAE Pulse Simulator</h1>
    <p style="text-align: center; color: #9ca3af; font-size: 1.1rem; margin-top: 5px;">
        Data Rescue + Campaign Simulation Dashboard
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        # Welcome message
        st.markdown("""
        <div class="info-card">
            <h3 style="color: #3b82f6; margin-top: 0;">👋 Welcome!</h3>
            <p style="color: #e0e0e0; margin-bottom: 0;">
                This dashboard helps you <strong>clean dirty data</strong> and <strong>simulate promotional campaigns</strong> 
                for UAE e-commerce operations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feature cards
        st.markdown("### ✨ Features")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_feature_card("📂", "Data Upload", "Load and preview your e-commerce data files"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_feature_card("🧹", "Data Rescue", "Detect & fix 15+ types of dirty data issues"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_feature_card("🎯", "Simulator", "Run what-if campaign scenarios"), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_feature_card("📊", "Analytics", "Visualize KPIs and trends"), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Load sample data button
        st.markdown("### 🚀 Get Started")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📥 Load Sample Data", use_container_width=True):
                with st.spinner("Loading sample data..."):
                    try:
                        products = pd.read_csv('data/products.csv')
                        stores = pd.read_csv('data/stores.csv')
                        sales = pd.read_csv('data/sales_raw.csv')
                        inventory = pd.read_csv('data/inventory_snapshot.csv')
                        
                        st.session_state.raw_products = products
                        st.session_state.raw_stores = stores
                        st.session_state.raw_sales = sales
                        st.session_state.raw_inventory = inventory
                        st.session_state.data_loaded = True
                        
                        st.success("✅ Sample data loaded successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error loading data: {str(e)}")
    
    else:
        # Data is loaded - show KPIs
        sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
        products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
        stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
        
        # Initialize simulator
        sim = Simulator()
        
        # Calculate KPIs
        kpis = sim.calculate_overall_kpis(sales_df, products_df)
        
        # Display KPI cards
        st.markdown("### 📈 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("Total Revenue", f"AED {kpis['total_revenue']:,.0f}"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card("Total Orders", f"{kpis['total_orders']:,}"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("Avg Order Value", f"AED {kpis['avg_order_value']:,.2f}"), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card("Profit Margin", f"{kpis['profit_margin_pct']:.1f}%"), unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("Total Profit", f"AED {kpis['total_profit']:,.0f}"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card("Total Units", f"{kpis['total_units']:,}"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("Return Rate", f"{kpis['return_rate_pct']:.1f}%"), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card("Avg Discount", f"{kpis['avg_discount_pct']:.1f}%"), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        st.markdown("### 📊 Quick Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by City
            city_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'city')
            if len(city_kpis) > 0:
                fig = px.pie(
                    city_kpis, 
                    values='revenue', 
                    names='city',
                    title='Revenue by City',
                    color_discrete_sequence=CHART_THEME['color_sequence'],
                    hole=0.4
                )
                fig = style_plotly_chart(fig)
                fig.update_traces(textposition='outside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Revenue by Channel
            channel_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'channel')
            if len(channel_kpis) > 0:
                fig = px.bar(
                    channel_kpis,
                    x='channel',
                    y='revenue',
                    title='Revenue by Channel',
                    color='channel',
                    color_discrete_sequence=CHART_THEME['color_sequence']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # Status cards
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.is_cleaned:
                st.markdown(create_success_card("Data has been cleaned and validated"), unsafe_allow_html=True)
            else:
                st.markdown(create_warning_card("Data not yet cleaned. Go to 🧹 Cleaner to validate and fix issues."), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_info_card(f"<strong>Data Source:</strong> {'Cleaned Data' if st.session_state.is_cleaned else 'Raw Data'}"), unsafe_allow_html=True)
    
    show_footer()

# ============================================================================
# PAGE: DATA
# ============================================================================

def show_data_page():
    """Display the data management page."""
    
    st.markdown("<h1>📂 Data Management</h1>", unsafe_allow_html=True)
    st.markdown("Upload, view, and manage your e-commerce data files.")
    
    st.markdown("---")
    
    # Upload section
    st.markdown("### 📤 Upload Data Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        products_file = st.file_uploader("Products CSV", type=['csv'], key='products_upload')
        sales_file = st.file_uploader("Sales CSV", type=['csv'], key='sales_upload')
    
    with col2:
        stores_file = st.file_uploader("Stores CSV", type=['csv'], key='stores_upload')
        inventory_file = st.file_uploader("Inventory CSV", type=['csv'], key='inventory_upload')
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Load Uploaded Files", use_container_width=True):
            try:
                if products_file:
                    st.session_state.raw_products = pd.read_csv(products_file)
                if stores_file:
                    st.session_state.raw_stores = pd.read_csv(stores_file)
                if sales_file:
                    st.session_state.raw_sales = pd.read_csv(sales_file)
                if inventory_file:
                    st.session_state.raw_inventory = pd.read_csv(inventory_file)
                
                st.session_state.data_loaded = True
                st.session_state.is_cleaned = False
                st.success("✅ Files uploaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    # Or load sample data
    st.markdown("### 📦 Or Use Sample Data")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Load Sample Data", use_container_width=True, key='sample_data_btn'):
            try:
                st.session_state.raw_products = pd.read_csv('data/products.csv')
                st.session_state.raw_stores = pd.read_csv('data/stores.csv')
                st.session_state.raw_sales = pd.read_csv('data/sales_raw.csv')
                st.session_state.raw_inventory = pd.read_csv('data/inventory_snapshot.csv')
                st.session_state.data_loaded = True
                st.session_state.is_cleaned = False
                st.success("✅ Sample data loaded!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Preview data
    if st.session_state.data_loaded:
        st.markdown("---")
        st.markdown("### 👀 Data Preview")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📦 Products", "🏪 Stores", "🛒 Sales", "📋 Inventory"])
        
        with tab1:
            if st.session_state.raw_products is not None:
                st.dataframe(st.session_state.raw_products.head(100), use_container_width=True)
                st.caption(f"Showing 100 of {len(st.session_state.raw_products)} rows")
        
        with tab2:
            if st.session_state.raw_stores is not None:
                st.dataframe(st.session_state.raw_stores.head(100), use_container_width=True)
                st.caption(f"Showing 100 of {len(st.session_state.raw_stores)} rows")
        
        with tab3:
            if st.session_state.raw_sales is not None:
                st.dataframe(st.session_state.raw_sales.head(100), use_container_width=True)
                st.caption(f"Showing 100 of {len(st.session_state.raw_sales)} rows")
        
        with tab4:
            if st.session_state.raw_inventory is not None:
                st.dataframe(st.session_state.raw_inventory.head(100), use_container_width=True)
                st.caption(f"Showing 100 of {len(st.session_state.raw_inventory)} rows")
    
    show_footer()

# ============================================================================
# PAGE: CLEANER
# ============================================================================

def show_cleaner_page():
    """Display the data cleaner page."""
    
    st.markdown("<h1>🧹 Data Rescue Center</h1>", unsafe_allow_html=True)
    st.markdown("Validate, detect issues, and clean your dirty data.")
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    # Clean data button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Data Cleaning", use_container_width=True, type="primary"):
            with st.spinner("Cleaning data... This may take a moment."):
                try:
                    cleaner = DataCleaner()
                    
                    clean_products, clean_stores, clean_sales, clean_inventory = cleaner.clean_all(
                        st.session_state.raw_products.copy(),
                        st.session_state.raw_stores.copy(),
                        st.session_state.raw_sales.copy(),
                        st.session_state.raw_inventory.copy()
                    )
                    
                    st.session_state.clean_products = clean_products
                    st.session_state.clean_stores = clean_stores
                    st.session_state.clean_sales = clean_sales
                    st.session_state.clean_inventory = clean_inventory
                    st.session_state.issues_df = cleaner.get_issues_df()
                    st.session_state.cleaner_stats = cleaner.stats
                    st.session_state.is_cleaned = True
                    
                    st.success("✅ Data cleaning complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error during cleaning: {str(e)}")
    
    # Show results if cleaned
    if st.session_state.is_cleaned:
        st.markdown("---")
        st.markdown("### 📊 Cleaning Results")
        
        stats = st.session_state.cleaner_stats
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            before = stats['products']['before']
            after = stats['products']['after']
            st.markdown(create_metric_card("Products", f"{after:,}", f"{before - after} removed", "negative" if before > after else "positive"), unsafe_allow_html=True)
        
        with col2:
            before = stats['stores']['before']
            after = stats['stores']['after']
            st.markdown(create_metric_card("Stores", f"{after:,}", f"{before - after} removed", "negative" if before > after else "positive"), unsafe_allow_html=True)
        
        with col3:
            before = stats['sales']['before']
            after = stats['sales']['after']
            st.markdown(create_metric_card("Sales", f"{after:,}", f"{before - after} removed", "negative" if before > after else "positive"), unsafe_allow_html=True)
        
        with col4:
            before = stats['inventory']['before']
            after = stats['inventory']['after']
            st.markdown(create_metric_card("Inventory", f"{after:,}", f"{before - after} removed", "negative" if before > after else "positive"), unsafe_allow_html=True)
        
        # Issues summary
        st.markdown("---")
        st.markdown("### 🔍 Issues Detected & Fixed")
        
        issues_df = st.session_state.issues_df
        
        if len(issues_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Issues by type
                issue_counts = issues_df['issue_type'].value_counts().reset_index()
                issue_counts.columns = ['Issue Type', 'Count']
                
                fig = px.bar(
                    issue_counts,
                    x='Count',
                    y='Issue Type',
                    orientation='h',
                    title='Issues by Type',
                    color='Count',
                    color_continuous_scale=['#3b82f6', '#8b5cf6', '#ec4899']
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Issues by table
                table_counts = issues_df['table'].value_counts().reset_index()
                table_counts.columns = ['Table', 'Count']
                
                fig = px.pie(
                    table_counts,
                    values='Count',
                    names='Table',
                    title='Issues by Table',
                    color_discrete_sequence=CHART_THEME['color_sequence'],
                    hole=0.4
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            # Issues table
            st.markdown("### 📋 Issues Log")
            st.dataframe(issues_df, use_container_width=True)
            
            # Download button
            csv = issues_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Issues Log",
                data=csv,
                file_name="issues_log.csv",
                mime="text/csv"
            )
        else:
            st.markdown(create_success_card("No issues found! Data is clean."), unsafe_allow_html=True)
    
    show_footer()

# ============================================================================
# PAGE: SIMULATOR
# ============================================================================

def show_simulator_page():
    """Display the campaign simulator page."""
    
    st.markdown("<h1>🎯 Campaign Simulator</h1>", unsafe_allow_html=True)
    st.markdown("Run what-if scenarios and forecast campaign outcomes.")
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    if not st.session_state.is_cleaned:
        st.markdown(create_warning_card("Please clean data first. Go to 🧹 Cleaner page."), unsafe_allow_html=True)
        show_footer()
        return
    
    # Campaign parameters
    st.markdown("### ⚙️ Campaign Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        discount_pct = st.slider("Discount %", 0, 50, 15, help="Discount percentage to offer")
        promo_budget = st.number_input("Promo Budget (AED)", 1000, 500000, 25000, step=5000)
    
    with col2:
        margin_floor = st.slider("Margin Floor %", 0, 50, 15, help="Minimum acceptable profit margin")
        campaign_days = st.slider("Campaign Days", 1, 30, 7)
    
    with col3:
        city = st.selectbox("Target City", ['All', 'Dubai', 'Abu Dhabi', 'Sharjah'])
        channel = st.selectbox("Target Channel", ['All', 'App', 'Web', 'Marketplace'])
        category = st.selectbox("Target Category", ['All', 'Electronics', 'Fashion', 'Grocery', 'Beauty', 'Home', 'Sports'])
    
    # Run simulation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_sim = st.button("🚀 Run Simulation", use_container_width=True, type="primary")
    
    if run_sim:
        with st.spinner("Running simulation..."):
            sim = Simulator()
            
            results = sim.simulate_campaign(
                st.session_state.clean_sales,
                st.session_state.clean_stores,
                st.session_state.clean_products,
                discount_pct=discount_pct,
                promo_budget=promo_budget,
                margin_floor=margin_floor,
                city=city,
                channel=channel,
                category=category,
                campaign_days=campaign_days
            )
            
            st.session_state.sim_results = results
    
    # Display results
    if 'sim_results' in st.session_state and st.session_state.sim_results:
        results = st.session_state.sim_results
        outputs = results['outputs']
        comparison = results['comparison']
        warnings = results['warnings']
        
        if outputs:
            st.markdown("---")
            st.markdown("### 📊 Simulation Results")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card("Expected Revenue", f"AED {outputs['expected_revenue']:,.0f}", f"{comparison['revenue_change_pct']:+.1f}%", "positive" if comparison['revenue_change_pct'] > 0 else "negative"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card("Expected Orders", f"{outputs['expected_orders']:,}", f"{comparison['order_change_pct']:+.1f}%", "positive" if comparison['order_change_pct'] > 0 else "negative"), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card("Net Profit", f"AED {outputs['expected_net_profit']:,.0f}", f"{comparison['profit_change_pct']:+.1f}%", "positive" if comparison['profit_change_pct'] > 0 else "negative"), unsafe_allow_html=True)
            
            with col4:
                roi_type = "positive" if outputs['roi_pct'] > 0 else "negative"
                st.markdown(create_metric_card("ROI", f"{outputs['roi_pct']:.1f}%", None), unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card("Demand Lift", f"+{outputs['demand_lift_pct']:.1f}%"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card("Margin", f"{outputs['expected_margin_pct']:.1f}%"), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card("Promo Cost", f"AED {outputs['promo_cost']:,.0f}"), unsafe_allow_html=True)
            
            with col4:
                st.markdown(create_metric_card("Fulfillment Cost", f"AED {outputs['fulfillment_cost']:,.0f}"), unsafe_allow_html=True)
            
            # Warnings
            if warnings:
                st.markdown("---")
                st.markdown("### ⚠️ Warnings")
                for warning in warnings:
                    st.markdown(create_warning_card(warning), unsafe_allow_html=True)
            
            # Comparison chart
            st.markdown("---")
            st.markdown("### 📈 Baseline vs Campaign")
            
            comp_data = pd.DataFrame({
                'Metric': ['Revenue', 'Profit', 'Orders'],
                'Baseline': [comparison['baseline_revenue'], comparison['baseline_profit'], comparison['baseline_orders']],
                'Campaign': [outputs['expected_revenue'], outputs['expected_net_profit'], outputs['expected_orders']]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Baseline', x=comp_data['Metric'], y=comp_data['Baseline'], marker_color='#3b82f6'))
            fig.add_trace(go.Bar(name='Campaign', x=comp_data['Metric'], y=comp_data['Campaign'], marker_color='#8b5cf6'))
            fig = style_plotly_chart(fig)
            fig.update_layout(barmode='group', title='Baseline vs Campaign Comparison')
            st.plotly_chart(fig, use_container_width=True)
    
    show_footer()

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================

def show_analytics_page():
    """Display the analytics page."""
    
    st.markdown("<h1>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Deep dive into your e-commerce performance metrics.")
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
    products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
    stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
    inventory_df = st.session_state.clean_inventory if st.session_state.is_cleaned else st.session_state.raw_inventory
    
    sim = Simulator()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏙️ By City", "📦 By Category", "📋 Inventory"])
    
    with tab1:
        st.markdown("### Daily Revenue Trend")
        daily_trends = sim.calculate_daily_trends(sales_df, products_df)
        
        if len(daily_trends) > 0:
            fig = px.line(
                daily_trends,
                x='date',
                y='revenue',
                title='Daily Revenue',
                color_discrete_sequence=['#8b5cf6']
            )
            fig = style_plotly_chart(fig)
            fig.update_traces(line=dict(width=3))
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.line(
                    daily_trends,
                    x='date',
                    y='orders',
                    title='Daily Orders',
                    color_discrete_sequence=['#3b82f6']
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(
                    daily_trends,
                    x='date',
                    y='profit',
                    title='Daily Profit',
                    color_discrete_sequence=['#10b981']
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Performance by City")
        city_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'city')
        
        if len(city_kpis) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    city_kpis,
                    x='city',
                    y='revenue',
                    title='Revenue by City',
                    color='city',
                    color_discrete_sequence=CHART_THEME['color_sequence']
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    city_kpis,
                    x='city',
                    y='profit_margin_pct',
                    title='Profit Margin by City',
                    color='city',
                    color_discrete_sequence=CHART_THEME['color_sequence']
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(city_kpis, use_container_width=True)
    
    with tab3:
        st.markdown("### Performance by Category")
        cat_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'category')
        
        if len(cat_kpis) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    cat_kpis,
                    values='revenue',
                    names='category',
                    title='Revenue Share by Category',
                    color_discrete_sequence=CHART_THEME['color_sequence'],
                    hole=0.4
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    cat_kpis,
                    x='category',
                    y='profit',
                    title='Profit by Category',
                    color='category',
                    color_discrete_sequence=CHART_THEME['color_sequence']
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(cat_kpis, use_container_width=True)
    
    with tab4:
        st.markdown("### Inventory Health")
        stockout = sim.calculate_stockout_risk(inventory_df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_metric_card("Total SKUs", f"{stockout['total_items']:,}"), unsafe_allow_html=True)
        
        with col2:
            risk_type = "negative" if stockout['stockout_risk_pct'] > 10 else "positive"
            st.markdown(create_metric_card("Stockout Risk", f"{stockout['stockout_risk_pct']:.1f}%"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("Zero Stock Items", f"{stockout['zero_stock']:,}"), unsafe_allow_html=True)
        
        # Inventory distribution
        if inventory_df is not None and 'stock_on_hand' in inventory_df.columns:
            fig = px.histogram(
                inventory_df,
                x='stock_on_hand',
                nbins=50,
                title='Stock Level Distribution',
                color_discrete_sequence=['#8b5cf6']
            )
            fig = style_plotly_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
    
    show_footer()

# ============================================================================
# MAIN ROUTING
# ============================================================================

if page == "🏠 Home":
    show_home_page()
elif page == "📂 Data":
    show_data_page()
elif page == "🧹 Cleaner":
    show_cleaner_page()
elif page == "🎯 Simulator":
    show_simulator_page()
elif page == "📊 Analytics":
    show_analytics_page()
