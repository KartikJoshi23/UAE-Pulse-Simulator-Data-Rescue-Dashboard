# ============================================================================
# UAE Pulse Simulator + Data Rescue Dashboard
# Main Streamlit Application - FIXED v3.0
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
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FIXED CSS - ALL ISSUES RESOLVED
# ============================================================================

st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== MAIN BACKGROUND ===== */
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #0d0d14 50%, #0a0a0f 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #111118 100%);
        border-right: 1px solid #1e1e2e;
    }
    
    /* ===== HEADINGS - SIMPLE COLORS, NO GRADIENT BOX ===== */
    h1 {
        color: #06b6d4 !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    h2 {
        color: #3b82f6 !important;
        font-weight: 600 !important;
    }
    
    h3 {
        color: #8b5cf6 !important;
        font-weight: 600 !important;
    }
    
    /* ===== METRIC CARDS - EXACT UNIFORM SIZE ===== */
    .metric-card {
        background: linear-gradient(145deg, #13131a 0%, #18181f 100%);
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #252532;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        height: 130px !important;
        min-height: 130px !important;
        max-height: 130px !important;
        box-sizing: border-box !important;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #06b6d4;
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.15);
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    
    .metric-value-cyan { color: #06b6d4; }
    .metric-value-blue { color: #3b82f6; }
    .metric-value-purple { color: #8b5cf6; }
    .metric-value-pink { color: #ec4899; }
    .metric-value-green { color: #10b981; }
    .metric-value-orange { color: #f59e0b; }
    .metric-value-teal { color: #14b8a6; }
    
    .metric-delta-positive {
        color: #10b981;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .metric-delta-negative {
        color: #ef4444;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* ===== FEATURE CARDS - EXACT UNIFORM SIZE ===== */
    .feature-card {
        background: linear-gradient(145deg, #13131a 0%, #18181f 100%);
        border-radius: 16px;
        padding: 30px 20px;
        border: 1px solid #252532;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        height: 200px !important;
        min-height: 200px !important;
        max-height: 200px !important;
        box-sizing: border-box !important;
        text-align: center;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(6, 182, 212, 0.12);
    }
    
    .feature-card-cyan:hover { border-color: #06b6d4; }
    .feature-card-blue:hover { border-color: #3b82f6; }
    .feature-card-purple:hover { border-color: #8b5cf6; }
    .feature-card-pink:hover { border-color: #ec4899; }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .feature-title-cyan { color: #06b6d4; }
    .feature-title-blue { color: #3b82f6; }
    .feature-title-purple { color: #8b5cf6; }
    .feature-title-pink { color: #ec4899; }
    
    .feature-desc {
        color: #94a3b8;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    /* ===== INFO/STATUS CARDS ===== */
    .info-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(59, 130, 246, 0.08) 100%);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #06b6d4;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateX(5px);
    }
    
    .success-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(20, 184, 166, 0.08) 100%);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #10b981;
        margin: 12px 0;
        color: #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .success-card:hover {
        transform: translateX(5px);
    }
    
    .warning-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(251, 146, 60, 0.08) 100%);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #f59e0b;
        margin: 12px 0;
        color: #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .warning-card:hover {
        transform: translateX(5px);
    }
    
    .error-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(236, 72, 153, 0.08) 100%);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #ef4444;
        margin: 12px 0;
        color: #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .error-card:hover {
        transform: translateX(5px);
    }
    
    /* ===== INSIGHT CARD ===== */
    .insight-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        border-radius: 12px;
        padding: 18px 22px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateX(5px);
        border-color: #8b5cf6;
    }
    
    .insight-title {
        color: #a78bfa;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .insight-text {
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* ===== MAIN NAV TABS ONLY - HOVER EFFECT ===== */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 5px;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: #13131a;
        border-radius: 10px;
        padding: 12px 15px;
        border: 1px solid #252532;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: #1a1a24;
        border-color: #06b6d4;
        transform: translateX(5px);
    }
    
    /* ===== SUB-TABS - NO HOVER TRANSFORM ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #13131a;
        border-radius: 10px;
        color: #94a3b8;
        padding: 10px 20px;
        border: 1px solid #252532;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0891b2 0%, #2563eb 100%);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.3);
        transform: translateY(-2px);
    }
    
    /* ===== FOOTER ===== */
    .footer {
        background: linear-gradient(135deg, #0d0d14 0%, #111118 100%);
        padding: 25px;
        text-align: center;
        border-top: 1px solid #252532;
        margin-top: 50px;
        border-radius: 16px 16px 0 0;
    }
    
    .footer-title {
        color: #e2e8f0;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .footer-subtitle {
        color: #64748b;
        font-size: 0.85rem;
        margin-bottom: 10px;
    }
    
    .footer-names {
        color: #06b6d4;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #252532, transparent);
        margin: 25px 0;
    }
    
    /* ===== HERO SECTION ===== */
    .hero-section {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
        border-radius: 20px;
        padding: 40px 35px;
        margin-bottom: 30px;
        border: 1px solid #252532;
        text-align: center;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 10px;
    }
    
    .hero-title span {
        color: #06b6d4;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 25px;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 6px 16px;
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0 5px;
    }
    
    /* ===== PAGE HEADER ===== */
    .page-header {
        margin-bottom: 5px;
    }
    
    .page-header h1 {
        margin-bottom: 5px !important;
    }
    
    .page-description {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    
</style>
""", unsafe_allow_html=True)
# ============================================================================
# HELPER FUNCTIONS FOR UI
# ============================================================================

def create_metric_card(label, value, delta=None, delta_type="positive", color="cyan"):
    """Create a styled metric card with EXACT uniform size."""
    delta_html = ""
    if delta:
        delta_class = "metric-delta-positive" if delta_type == "positive" else "metric-delta-negative"
        delta_icon = "↑" if delta_type == "positive" else "↓"
        delta_html = f'<div class="{delta_class}">{delta_icon} {delta}</div>'
    else:
        delta_html = '<div style="height: 20px;"></div>'  # Spacer for uniform height
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value metric-value-{color}">{value}</div>
        {delta_html}
    </div>
    """

def create_feature_card(icon, title, description, color="cyan"):
    """Create a feature card with EXACT uniform size."""
    return f"""
    <div class="feature-card feature-card-{color}">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title feature-title-{color}">{title}</div>
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

def create_insight_card(title, insight_text):
    """Create a business insight card."""
    return f"""
    <div class="insight-card">
        <div class="insight-title">💡 {title}</div>
        <div class="insight-text">{insight_text}</div>
    </div>
    """

def show_footer():
    """Display the footer with team names."""
    st.markdown("""
    <div class="footer">
        <div class="footer-title">🚀 UAE Pulse Simulator + Data Rescue Dashboard</div>
        <div class="footer-subtitle">Built with ❤️ by</div>
        <div class="footer-names">Kartik Joshi • Gagandeep Singh • Samuel Alex • Prem Kukreja</div>
    </div>
    """, unsafe_allow_html=True)

def generate_insights(kpis, city_kpis=None, channel_kpis=None, cat_kpis=None):
    """Generate business insights based on KPIs."""
    insights = []
    
    # Revenue insight
    if kpis.get('total_revenue', 0) > 0:
        aov = kpis.get('avg_order_value', 0)
        if aov > 500:
            insights.append(("High-Value Customers", f"Average order value is AED {aov:,.0f}, indicating premium customer segment. Consider upselling strategies."))
        elif aov < 200:
            insights.append(("Growth Opportunity", f"Average order value is AED {aov:,.0f}. Bundle offers could increase basket size by 15-25%."))
    
    # Margin insight
    margin = kpis.get('profit_margin_pct', 0)
    if margin > 25:
        insights.append(("Strong Margins", f"Profit margin at {margin:.1f}% is healthy. Room for strategic discounts without hurting profitability."))
    elif margin < 15:
        insights.append(("Margin Alert", f"Profit margin at {margin:.1f}% is below industry benchmark. Review pricing strategy and costs."))
    
    # Return rate insight
    return_rate = kpis.get('return_rate_pct', 0)
    if return_rate > 10:
        insights.append(("High Returns", f"Return rate of {return_rate:.1f}% is above normal. Investigate product quality or description accuracy."))
    elif return_rate < 3:
        insights.append(("Excellent Quality", f"Low return rate of {return_rate:.1f}% indicates high customer satisfaction."))
    
    # City insight
    if city_kpis is not None and len(city_kpis) > 0:
        top_city = city_kpis.iloc[0]['city'] if 'city' in city_kpis.columns else None
        if top_city:
            top_revenue = city_kpis.iloc[0]['revenue']
            total_revenue = city_kpis['revenue'].sum()
            pct = (top_revenue / total_revenue * 100) if total_revenue > 0 else 0
            insights.append(("Market Concentration", f"{top_city} contributes {pct:.0f}% of total revenue. {'Diversify to reduce risk.' if pct > 50 else 'Healthy market distribution.'}"))
    
    # Channel insight
    if channel_kpis is not None and len(channel_kpis) > 0:
        top_channel = channel_kpis.iloc[0]['channel'] if 'channel' in channel_kpis.columns else None
        if top_channel:
            insights.append(("Channel Performance", f"{top_channel} is your top-performing channel. Optimize marketing spend accordingly."))
    
    return insights[:3]  # Return top 3 insights

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
        <div style="font-size: 2.5rem; margin-bottom: 8px;">🚀</div>
        <h2 style="color: #06b6d4 !important; font-size: 1.4rem; margin-bottom: 3px;">UAE Pulse</h2>
        <p style="color: #64748b; font-size: 0.8rem;">Simulator + Data Rescue</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown('<p style="color: #06b6d4; font-weight: 600; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 12px;">📍 NAVIGATION</p>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📂 Data", "🧹 Cleaner", "🎯 Simulator", "📊 Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Data Status
    st.markdown('<p style="color: #3b82f6; font-weight: 600; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 12px;">📡 STATUS</p>', unsafe_allow_html=True)
    
    data_loaded = st.session_state.data_loaded
    data_cleaned = st.session_state.is_cleaned
    
    status_color_loaded = "#10b981" if data_loaded else "#ef4444"
    status_color_cleaned = "#10b981" if data_cleaned else "#f59e0b" if data_loaded else "#ef4444"
    
    st.markdown(f"""
    <div style="background: #13131a; border-radius: 10px; padding: 12px; border: 1px solid #252532;">
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color_loaded}; margin-right: 10px; box-shadow: 0 0 8px {status_color_loaded};"></div>
            <span style="color: #e2e8f0; font-size: 0.85rem;">Data Loaded</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color_cleaned}; margin-right: 10px; box-shadow: 0 0 8px {status_color_cleaned};"></div>
            <span style="color: #e2e8f0; font-size: 0.85rem;">Data Cleaned</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats (only if data loaded)
    if st.session_state.data_loaded:
        st.markdown("---")
        st.markdown('<p style="color: #8b5cf6; font-weight: 600; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 12px;">📈 QUICK STATS</p>', unsafe_allow_html=True)
        
        sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
        if sales_df is not None:
            total_records = len(sales_df)
            total_revenue = (sales_df['qty'] * sales_df['selling_price_aed']).sum() if 'qty' in sales_df.columns else 0
            
            st.markdown(f"""
            <div style="background: #13131a; border-radius: 10px; padding: 12px; border: 1px solid #252532;">
                <div style="margin-bottom: 10px;">
                    <span style="color: #64748b; font-size: 0.75rem;">RECORDS</span><br>
                    <span style="color: #06b6d4; font-weight: 700; font-size: 1.2rem;">{total_records:,}</span>
                </div>
                <div>
                    <span style="color: #64748b; font-size: 0.75rem;">REVENUE</span><br>
                    <span style="color: #10b981; font-weight: 700; font-size: 1rem;">AED {total_revenue:,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PAGE: HOME
# ============================================================================

def show_home_page():
    """Display the home page."""
    
    if not st.session_state.data_loaded:
        # ===== HERO SECTION =====
        st.markdown("""
        <div class="hero-section">
            <div class="hero-badge">✨ UAE E-Commerce</div>
            <div class="hero-badge" style="background: linear-gradient(135deg, #8b5cf6, #ec4899);">v3.0</div>
            <h1 class="hero-title">🚀 <span>UAE Pulse</span> Simulator</h1>
            <p class="hero-subtitle">Transform dirty data into actionable insights. Clean, simulate, and visualize.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== FEATURES =====
        st.markdown("### ✨ Powerful Features")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_feature_card("📂", "Data Upload", "Upload and preview your e-commerce CSV files", "cyan"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_feature_card("🧹", "Data Rescue", "Auto-fix 15+ types of data quality issues", "blue"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_feature_card("🎯", "Simulator", "Run what-if scenarios and forecast ROI", "purple"), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_feature_card("📊", "Analytics", "Interactive KPI dashboards and trends", "pink"), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ===== CAPABILITIES =====
        st.markdown("### 🔥 What You Can Do")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4 style="color: #06b6d4; margin-top: 0; font-size: 1rem;">🧹 Data Cleaning</h4>
                <ul style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0; padding-left: 20px;">
                    <li>Missing values & duplicates</li>
                    <li>Outliers & negative values</li>
                    <li>Format standardization</li>
                    <li>FK violations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-card" style="border-left-color: #8b5cf6;">
                <h4 style="color: #8b5cf6; margin-top: 0; font-size: 1rem;">🎯 Simulation</h4>
                <ul style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0; padding-left: 20px;">
                    <li>Discount impact modeling</li>
                    <li>Category elasticity</li>
                    <li>ROI forecasting</li>
                    <li>Risk alerts</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ===== GET STARTED =====
        st.markdown("### 🚀 Get Started")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📥 Load Sample Data & Explore", use_container_width=True):
                with st.spinner("Loading sample data..."):
                    try:
                        st.session_state.raw_products = pd.read_csv('data/products.csv')
                        st.session_state.raw_stores = pd.read_csv('data/stores.csv')
                        st.session_state.raw_sales = pd.read_csv('data/sales_raw.csv')
                        st.session_state.raw_inventory = pd.read_csv('data/inventory_snapshot.csv')
                        st.session_state.data_loaded = True
                        st.success("✅ Sample data loaded!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    else:
        # ===== DATA LOADED - SHOW DASHBOARD =====
        sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
        products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
        stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
        
        # Page Header
        st.markdown('<div class="page-header"><h1>📊 Performance Dashboard</h1></div>', unsafe_allow_html=True)
        st.markdown('<p class="page-description">Real-time insights from your e-commerce data</p>', unsafe_allow_html=True)
        
        sim = Simulator()
        kpis = sim.calculate_overall_kpis(sales_df, products_df)
        
        # ===== KPI ROW 1 =====
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("Total Revenue", f"AED {kpis['total_revenue']:,.0f}", color="cyan"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_metric_card("Total Orders", f"{kpis['total_orders']:,}", color="blue"), unsafe_allow_html=True)
        with col3:
            st.markdown(create_metric_card("Avg Order Value", f"AED {kpis['avg_order_value']:,.0f}", color="purple"), unsafe_allow_html=True)
        with col4:
            st.markdown(create_metric_card("Profit Margin", f"{kpis['profit_margin_pct']:.1f}%", color="green"), unsafe_allow_html=True)
        
        # ===== KPI ROW 2 =====
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("Total Profit", f"AED {kpis['total_profit']:,.0f}", color="teal"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_metric_card("Total Units", f"{kpis['total_units']:,}", color="orange"), unsafe_allow_html=True)
        with col3:
            st.markdown(create_metric_card("Return Rate", f"{kpis['return_rate_pct']:.1f}%", color="pink"), unsafe_allow_html=True)
        with col4:
            st.markdown(create_metric_card("Avg Discount", f"{kpis['avg_discount_pct']:.1f}%", color="blue"), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== CHARTS =====
        st.markdown("### 📈 Quick Overview")
        
        col1, col2 = st.columns(2)
        
        city_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'city')
        channel_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'channel')
        
        with col1:
            if len(city_kpis) > 0:
                fig = px.pie(city_kpis, values='revenue', names='city', title='Revenue by City',
                            color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6'], hole=0.45)
                fig = style_plotly_chart(fig)
                fig.update_traces(textposition='outside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if len(channel_kpis) > 0:
                fig = px.bar(channel_kpis, x='channel', y='revenue', title='Revenue by Channel',
                            color='channel', color_discrete_sequence=['#10b981', '#f59e0b', '#ec4899'])
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # ===== BUSINESS INSIGHTS =====
        st.markdown("---")
        st.markdown("### 💡 Key Business Insights")
        
        insights = generate_insights(kpis, city_kpis, channel_kpis)
        
        for title, text in insights:
            st.markdown(create_insight_card(title, text), unsafe_allow_html=True)
        
        # ===== STATUS =====
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.is_cleaned:
                st.markdown(create_success_card("Data cleaned and validated. Ready for simulation!"), unsafe_allow_html=True)
            else:
                st.markdown(create_warning_card("Data not cleaned yet. Go to 🧹 Cleaner for better accuracy."), unsafe_allow_html=True)
        
        with col2:
            source = "Cleaned Data ✨" if st.session_state.is_cleaned else "Raw Data 📥"
            st.markdown(create_info_card(f"<strong>Source:</strong> {source}"), unsafe_allow_html=True)
    
    show_footer()
    # ============================================================================
# PAGE: DATA
# ============================================================================

def show_data_page():
    """Display the data management page."""
    
    st.markdown('<div class="page-header"><h1>📂 Data Management</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Upload, view, and manage your e-commerce data files</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload section
    st.markdown("### 📤 Upload Data Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        products_file = st.file_uploader("📦 Products CSV", type=['csv'], key='products_upload')
        sales_file = st.file_uploader("🛒 Sales CSV", type=['csv'], key='sales_upload')
    
    with col2:
        stores_file = st.file_uploader("🏪 Stores CSV", type=['csv'], key='stores_upload')
        inventory_file = st.file_uploader("📋 Inventory CSV", type=['csv'], key='inventory_upload')
    
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
    
    # Sample data option
    st.markdown("### 📦 Or Use Sample Data")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Load Sample Data", use_container_width=True, key='sample_btn'):
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
    
    # Data preview
    if st.session_state.data_loaded:
        st.markdown("---")
        st.markdown("### 👀 Data Preview")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📦 Products", "🏪 Stores", "🛒 Sales", "📋 Inventory"])
        
        with tab1:
            if st.session_state.raw_products is not None:
                df = st.session_state.raw_products
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(create_metric_card("Rows", f"{len(df):,}", color="cyan"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_metric_card("Columns", f"{len(df.columns)}", color="blue"), unsafe_allow_html=True)
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 0
                    st.markdown(create_metric_card("Null %", f"{null_pct:.1f}%", color="orange"), unsafe_allow_html=True)
                st.dataframe(df.head(50), use_container_width=True)
        
        with tab2:
            if st.session_state.raw_stores is not None:
                df = st.session_state.raw_stores
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(create_metric_card("Rows", f"{len(df):,}", color="cyan"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_metric_card("Columns", f"{len(df.columns)}", color="blue"), unsafe_allow_html=True)
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 0
                    st.markdown(create_metric_card("Null %", f"{null_pct:.1f}%", color="orange"), unsafe_allow_html=True)
                st.dataframe(df.head(50), use_container_width=True)
        
        with tab3:
            if st.session_state.raw_sales is not None:
                df = st.session_state.raw_sales
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(create_metric_card("Rows", f"{len(df):,}", color="cyan"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_metric_card("Columns", f"{len(df.columns)}", color="blue"), unsafe_allow_html=True)
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 0
                    st.markdown(create_metric_card("Null %", f"{null_pct:.1f}%", color="orange"), unsafe_allow_html=True)
                st.dataframe(df.head(50), use_container_width=True)
        
        with tab4:
            if st.session_state.raw_inventory is not None:
                df = st.session_state.raw_inventory
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(create_metric_card("Rows", f"{len(df):,}", color="cyan"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_metric_card("Columns", f"{len(df.columns)}", color="blue"), unsafe_allow_html=True)
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 0
                    st.markdown(create_metric_card("Null %", f"{null_pct:.1f}%", color="orange"), unsafe_allow_html=True)
                st.dataframe(df.head(50), use_container_width=True)
        
        # Data Quality Insight
        st.markdown("---")
        st.markdown("### 💡 Data Quality Insight")
        
        total_nulls = 0
        total_cells = 0
        for df in [st.session_state.raw_products, st.session_state.raw_stores, st.session_state.raw_sales, st.session_state.raw_inventory]:
            if df is not None:
                total_nulls += df.isnull().sum().sum()
                total_cells += len(df) * len(df.columns)
        
        overall_null_pct = (total_nulls / total_cells * 100) if total_cells > 0 else 0
        
        if overall_null_pct > 5:
            st.markdown(create_insight_card("Data Quality Alert", f"Overall null rate is {overall_null_pct:.1f}%. Recommend running Data Cleaner to fix missing values and improve data quality."), unsafe_allow_html=True)
        elif overall_null_pct > 0:
            st.markdown(create_insight_card("Minor Issues", f"Overall null rate is {overall_null_pct:.1f}%. Data Cleaner can help fix these issues."), unsafe_allow_html=True)
        else:
            st.markdown(create_insight_card("Good Quality", "No missing values detected! Data looks clean."), unsafe_allow_html=True)
    
    show_footer()

# ============================================================================
# PAGE: CLEANER
# ============================================================================

def show_cleaner_page():
    """Display the data cleaner page."""
    
    st.markdown('<div class="page-header"><h1>🧹 Data Rescue Center</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Validate, detect issues, and clean your dirty data automatically</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    # Issue types
    st.markdown("### 🔍 Issues We Detect & Fix")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <strong style="color: #06b6d4;">Data Quality</strong>
            <ul style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0; padding-left: 18px;">
                <li>Missing values</li>
                <li>Duplicate records</li>
                <li>Whitespace issues</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="border-left-color: #8b5cf6;">
            <strong style="color: #8b5cf6;">Format Issues</strong>
            <ul style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0; padding-left: 18px;">
                <li>Invalid timestamps</li>
                <li>Mixed case values</li>
                <li>Boolean strings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card" style="border-left-color: #ec4899;">
            <strong style="color: #ec4899;">Value Issues</strong>
            <ul style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0; padding-left: 18px;">
                <li>Negative values</li>
                <li>Outliers</li>
                <li>FK violations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clean button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Data Cleaning", use_container_width=True, type="primary"):
            with st.spinner("Cleaning data..."):
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
                    st.error(f"❌ Error: {str(e)}")
    
    # Results
    if st.session_state.is_cleaned:
        st.markdown("---")
        st.markdown("### 📊 Cleaning Results")
        
        stats = st.session_state.cleaner_stats
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            before, after = stats['products']['before'], stats['products']['after']
            delta = f"{before - after} fixed" if before > after else "No change"
            st.markdown(create_metric_card("Products", f"{after:,}", delta, "negative" if before > after else "positive", "cyan"), unsafe_allow_html=True)
        
        with col2:
            before, after = stats['stores']['before'], stats['stores']['after']
            delta = f"{before - after} fixed" if before > after else "No change"
            st.markdown(create_metric_card("Stores", f"{after:,}", delta, "negative" if before > after else "positive", "blue"), unsafe_allow_html=True)
        
        with col3:
            before, after = stats['sales']['before'], stats['sales']['after']
            delta = f"{before - after} fixed" if before > after else "No change"
            st.markdown(create_metric_card("Sales", f"{after:,}", delta, "negative" if before > after else "positive", "purple"), unsafe_allow_html=True)
        
        with col4:
            before, after = stats['inventory']['before'], stats['inventory']['after']
            delta = f"{before - after} fixed" if before > after else "No change"
            st.markdown(create_metric_card("Inventory", f"{after:,}", delta, "negative" if before > after else "positive", "pink"), unsafe_allow_html=True)
        
        # Issues details
        st.markdown("---")
        st.markdown("### 🔍 Issues Detected & Fixed")
        
        issues_df = st.session_state.issues_df
        
        if len(issues_df) > 0:
            st.markdown(create_success_card(f"Total {len(issues_df)} issues detected and fixed!"), unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                issue_counts = issues_df['issue_type'].value_counts().reset_index()
                issue_counts.columns = ['Issue Type', 'Count']
                fig = px.bar(issue_counts, x='Count', y='Issue Type', orientation='h', title='Issues by Type',
                            color='Count', color_continuous_scale=['#06b6d4', '#3b82f6', '#8b5cf6'])
                fig = style_plotly_chart(fig)
                fig.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                table_counts = issues_df['table'].value_counts().reset_index()
                table_counts.columns = ['Table', 'Count']
                fig = px.pie(table_counts, values='Count', names='Table', title='Issues by Table',
                            color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899'], hole=0.45)
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            # Cleaning Insight
            st.markdown("### 💡 Cleaning Insight")
            
            top_issue = issues_df['issue_type'].value_counts().idxmax()
            top_count = issues_df['issue_type'].value_counts().max()
            st.markdown(create_insight_card("Top Issue", f"'{top_issue}' was the most common issue with {top_count} occurrences. This has been automatically fixed."), unsafe_allow_html=True)
            
            # Issues log
            st.markdown("### 📋 Issues Log")
            st.dataframe(issues_df, use_container_width=True)
            
            csv = issues_df.to_csv(index=False)
            st.download_button("📥 Download Issues Log", csv, "issues_log.csv", "text/csv")
        else:
            st.markdown(create_success_card("No issues found! Data is already clean."), unsafe_allow_html=True)
    
    show_footer()

# ============================================================================
# PAGE: SIMULATOR
# ============================================================================

def show_simulator_page():
    """Display the campaign simulator page."""
    
    st.markdown('<div class="page-header"><h1>🎯 Campaign Simulator</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Run what-if scenarios and forecast campaign outcomes</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    if not st.session_state.is_cleaned:
        st.markdown(create_warning_card("Recommend cleaning data first for accurate results. Go to 🧹 Cleaner."), unsafe_allow_html=True)
    
    # Parameters
    st.markdown("### ⚙️ Campaign Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<p style="color: #06b6d4; font-weight: 600; font-size: 0.85rem;">💰 PRICING</p>', unsafe_allow_html=True)
        discount_pct = st.slider("Discount %", 0, 50, 15)
        promo_budget = st.number_input("Promo Budget (AED)", 1000, 500000, 25000, step=5000)
    
    with col2:
        st.markdown('<p style="color: #8b5cf6; font-weight: 600; font-size: 0.85rem;">📊 CONSTRAINTS</p>', unsafe_allow_html=True)
        margin_floor = st.slider("Margin Floor %", 0, 50, 15)
        campaign_days = st.slider("Campaign Days", 1, 30, 7)
    
    with col3:
        st.markdown('<p style="color: #ec4899; font-weight: 600; font-size: 0.85rem;">🎯 TARGETING</p>', unsafe_allow_html=True)
        city = st.selectbox("City", ['All', 'Dubai', 'Abu Dhabi', 'Sharjah'])
        channel = st.selectbox("Channel", ['All', 'App', 'Web', 'Marketplace'])
        category = st.selectbox("Category", ['All', 'Electronics', 'Fashion', 'Grocery', 'Beauty', 'Home', 'Sports'])
    
    st.markdown("---")
    
    # Run button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_sim = st.button("🚀 Run Simulation", use_container_width=True, type="primary")
    
    if run_sim:
        with st.spinner("Running simulation..."):
            sim = Simulator()
            
            sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
            stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
            products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
            
            results = sim.simulate_campaign(
                sales_df, stores_df, products_df,
                discount_pct=discount_pct, promo_budget=promo_budget, margin_floor=margin_floor,
                city=city, channel=channel, category=category, campaign_days=campaign_days
            )
            
            st.session_state.sim_results = results
    
    # Results
    if 'sim_results' in st.session_state and st.session_state.sim_results:
        results = st.session_state.sim_results
        outputs = results['outputs']
        comparison = results['comparison']
        warnings = results['warnings']
        
        if outputs:
            st.markdown("---")
            st.markdown("### 📊 Simulation Results")
            
            # Row 1
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                delta = f"{comparison['revenue_change_pct']:+.1f}%"
                st.markdown(create_metric_card("Expected Revenue", f"AED {outputs['expected_revenue']:,.0f}", delta, "positive" if comparison['revenue_change_pct'] > 0 else "negative", "cyan"), unsafe_allow_html=True)
            with col2:
                delta = f"{comparison['order_change_pct']:+.1f}%"
                st.markdown(create_metric_card("Expected Orders", f"{outputs['expected_orders']:,}", delta, "positive" if comparison['order_change_pct'] > 0 else "negative", "blue"), unsafe_allow_html=True)
            with col3:
                delta = f"{comparison['profit_change_pct']:+.1f}%"
                st.markdown(create_metric_card("Net Profit", f"AED {outputs['expected_net_profit']:,.0f}", delta, "positive" if comparison['profit_change_pct'] > 0 else "negative", "green"), unsafe_allow_html=True)
            with col4:
                st.markdown(create_metric_card("ROI", f"{outputs['roi_pct']:.1f}%", color="teal" if outputs['roi_pct'] > 0 else "pink"), unsafe_allow_html=True)
            
            # Row 2
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card("Demand Lift", f"+{outputs['demand_lift_pct']:.1f}%", color="purple"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_metric_card("Margin", f"{outputs['expected_margin_pct']:.1f}%", color="green" if outputs['expected_margin_pct'] >= margin_floor else "orange"), unsafe_allow_html=True)
            with col3:
                st.markdown(create_metric_card("Promo Cost", f"AED {outputs['promo_cost']:,.0f}", color="orange"), unsafe_allow_html=True)
            with col4:
                st.markdown(create_metric_card("Fulfillment", f"AED {outputs['fulfillment_cost']:,.0f}", color="blue"), unsafe_allow_html=True)
            
            # Warnings
            if warnings:
                st.markdown("---")
                st.markdown("### ⚠️ Risk Alerts")
                for w in warnings:
                    st.markdown(create_warning_card(w), unsafe_allow_html=True)
            else:
                st.markdown("---")
                st.markdown(create_success_card("All metrics healthy. Campaign looks profitable!"), unsafe_allow_html=True)
            
            # Simulation Insight
            st.markdown("---")
            st.markdown("### 💡 Simulation Insight")
            
            if outputs['roi_pct'] > 100:
                st.markdown(create_insight_card("High ROI Campaign", f"Expected ROI of {outputs['roi_pct']:.0f}% is excellent. This campaign is highly profitable."), unsafe_allow_html=True)
            elif outputs['roi_pct'] > 0:
                st.markdown(create_insight_card("Profitable Campaign", f"Expected ROI of {outputs['roi_pct']:.0f}% is positive. Consider increasing budget for more impact."), unsafe_allow_html=True)
            else:
                st.markdown(create_insight_card("Review Needed", f"Negative ROI of {outputs['roi_pct']:.0f}%. Consider reducing discount or targeting higher-margin categories."), unsafe_allow_html=True)
            
            # Chart
            st.markdown("---")
            st.markdown("### 📈 Baseline vs Campaign")
            
            col1, col2 = st.columns(2)
            
            with col1:
                comp_data = pd.DataFrame({
                    'Metric': ['Revenue', 'Profit'],
                    'Baseline': [comparison['baseline_revenue'], comparison['baseline_profit']],
                    'Campaign': [outputs['expected_revenue'], outputs['expected_net_profit']]
                })
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Baseline', x=comp_data['Metric'], y=comp_data['Baseline'], marker_color='#3b82f6'))
                fig.add_trace(go.Bar(name='Campaign', x=comp_data['Metric'], y=comp_data['Campaign'], marker_color='#06b6d4'))
                fig = style_plotly_chart(fig)
                fig.update_layout(barmode='group', title='Revenue & Profit')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                orders_data = pd.DataFrame({'Type': ['Baseline', 'Campaign'], 'Orders': [comparison['baseline_orders'], outputs['expected_orders']]})
                fig = px.bar(orders_data, x='Type', y='Orders', title='Orders Comparison', color='Type', color_discrete_sequence=['#8b5cf6', '#ec4899'])
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    show_footer()

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================

def show_analytics_page():
    """Display the analytics page."""
    
    st.markdown('<div class="page-header"><h1>📊 Analytics Dashboard</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Deep dive into your e-commerce performance metrics</p>', unsafe_allow_html=True)
    
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
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏙️ By City", "📦 By Category", "📋 Inventory"])
    
    with tab1:
        st.markdown("### 📈 Daily Performance Trends")
        daily = sim.calculate_daily_trends(sales_df, products_df)
        
        if len(daily) > 0:
            fig = px.area(daily, x='date', y='revenue', title='Daily Revenue', color_discrete_sequence=['#06b6d4'])
            fig = style_plotly_chart(fig)
            fig.update_traces(line=dict(width=2), fillcolor='rgba(6, 182, 212, 0.2)')
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.line(daily, x='date', y='orders', title='Daily Orders', color_discrete_sequence=['#3b82f6'])
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.line(daily, x='date', y='profit', title='Daily Profit', color_discrete_sequence=['#10b981'])
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            # Trend Insight
            st.markdown("### 💡 Trend Insight")
            avg_revenue = daily['revenue'].mean()
            max_revenue = daily['revenue'].max()
            max_date = daily.loc[daily['revenue'].idxmax(), 'date']
            st.markdown(create_insight_card("Peak Performance", f"Best day was {max_date.strftime('%b %d')} with AED {max_revenue:,.0f} revenue ({(max_revenue/avg_revenue-1)*100:.0f}% above average)."), unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🏙️ Performance by City")
        city_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'city')
        
        if len(city_kpis) > 0:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(city_kpis, x='city', y='revenue', title='Revenue by City', color='city', color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6'])
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(city_kpis, x='city', y='profit_margin_pct', title='Margin by City', color='city', color_discrete_sequence=['#10b981', '#14b8a6', '#06b6d4'])
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(city_kpis, use_container_width=True)
            
            # City Insight
            st.markdown("### 💡 City Insight")
            top_city = city_kpis.iloc[0]
            st.markdown(create_insight_card("Top Market", f"{top_city['city']} leads with AED {top_city['revenue']:,.0f} revenue and {top_city['profit_margin_pct']:.1f}% margin."), unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📦 Performance by Category")
        cat_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'category')
        
        if len(cat_kpis) > 0:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(cat_kpis, values='revenue', names='category', title='Revenue Share', color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'], hole=0.45)
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(cat_kpis, x='category', y='profit', title='Profit by Category', color='profit', color_continuous_scale=['#3b82f6', '#8b5cf6', '#ec4899'])
                fig = style_plotly_chart(fig)
                fig.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(cat_kpis, use_container_width=True)
            
            # Category Insight
            st.markdown("### 💡 Category Insight")
            top_cat = cat_kpis.iloc[0]
            st.markdown(create_insight_card("Best Category", f"{top_cat['category']} is your top performer with AED {top_cat['revenue']:,.0f} revenue. Focus marketing here for quick wins."), unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📋 Inventory Health")
        stockout = sim.calculate_stockout_risk(inventory_df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(create_metric_card("Total SKUs", f"{stockout['total_items']:,}", color="cyan"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_metric_card("Stockout Risk", f"{stockout['stockout_risk_pct']:.1f}%", color="orange" if stockout['stockout_risk_pct'] > 10 else "green"), unsafe_allow_html=True)
        with col3:
            st.markdown(create_metric_card("Zero Stock", f"{stockout['zero_stock']:,}", color="pink" if stockout['zero_stock'] > 0 else "green"), unsafe_allow_html=True)
        
        st.markdown("---")
        
        if inventory_df is not None and 'stock_on_hand' in inventory_df.columns:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(inventory_df, x='stock_on_hand', nbins=30, title='Stock Distribution', color_discrete_sequence=['#8b5cf6'])
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                inv_copy = inventory_df.copy()
                inv_copy['status'] = inv_copy.apply(lambda x: 'Critical' if x['stock_on_hand'] == 0 else ('Low' if x['stock_on_hand'] <= x.get('reorder_point', 10) else 'Healthy'), axis=1)
                status_counts = inv_copy['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                fig = px.pie(status_counts, values='Count', names='Status', title='Inventory Status', color='Status', color_discrete_map={'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'}, hole=0.45)
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            # Inventory Insight
            st.markdown("### 💡 Inventory Insight")
            if stockout['zero_stock'] > 0:
                st.markdown(create_insight_card("Stock Alert", f"{stockout['zero_stock']} items are out of stock. Immediate reorder needed to prevent lost sales."), unsafe_allow_html=True)
            elif stockout['stockout_risk_pct'] > 15:
                st.markdown(create_insight_card("Reorder Soon", f"{stockout['stockout_risk_pct']:.0f}% of inventory is below reorder point. Plan replenishment soon."), unsafe_allow_html=True)
            else:
                st.markdown(create_insight_card("Healthy Stock", "Inventory levels are healthy. Continue monitoring."), unsafe_allow_html=True)
    
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
