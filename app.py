# ============================================================================
# UAE Pulse Simulator + Data Rescue Dashboard
# Main Streamlit Application - ENHANCED UI v2.0
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
# ENHANCED CSS - MULTI-COLOR DARK THEME WITH ANIMATIONS
# ============================================================================

st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: #16161f;
        --bg-card-hover: #1e1e2d;
        
        --accent-cyan: #06b6d4;
        --accent-blue: #3b82f6;
        --accent-purple: #8b5cf6;
        --accent-pink: #ec4899;
        --accent-green: #10b981;
        --accent-orange: #f59e0b;
        --accent-red: #ef4444;
        --accent-teal: #14b8a6;
        
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        
        --border-color: #2d2d3a;
        --border-glow: rgba(6, 182, 212, 0.3);
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.2);
        }
        50% {
            box-shadow: 0 0 40px rgba(6, 182, 212, 0.4);
        }
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
    
    @keyframes borderGlow {
        0%, 100% {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
        }
        33% {
            border-color: var(--accent-purple);
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
        }
        66% {
            border-color: var(--accent-pink);
            box-shadow: 0 0 15px rgba(236, 72, 153, 0.3);
        }
    }
    
    /* ===== REMOVE DEFAULT STREAMLIT ELEMENTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== MAIN BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0f0f18 25%, #12121a 50%, #0f0f18 75%, #0a0a0f 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f18 0%, #12121a 50%, #0a0a0f 100%);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 2px;
        height: 100%;
        background: linear-gradient(180deg, var(--accent-cyan), var(--accent-purple), var(--accent-pink));
        opacity: 0.5;
    }
    
    /* ===== HEADERS ===== */
    h1 {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 50%, var(--accent-purple) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        animation: fadeInUp 0.6s ease-out;
    }
    
    h2 {
        color: var(--accent-cyan) !important;
        font-weight: 600 !important;
    }
    
    h3 {
        background: linear-gradient(90deg, var(--accent-teal), var(--accent-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600 !important;
    }
    
    /* ===== HERO SECTION ===== */
    .hero-container {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.1) 50%, rgba(236, 72, 153, 0.1) 100%);
        border-radius: 24px;
        padding: 50px 40px;
        margin-bottom: 30px;
        border: 1px solid rgba(6, 182, 212, 0.2);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 50%);
        animation: float 6s ease-in-out infinite;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, var(--accent-cyan) 50%, var(--accent-purple) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 8px 20px;
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
        border-radius: 50px;
        color: white;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }
    
    /* ===== METRIC CARDS - UNIFORM SIZE ===== */
    .metric-card {
        background: linear-gradient(145deg, #16161f 0%, #1a1a24 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        border-color: var(--accent-cyan);
        box-shadow: 0 12px 40px rgba(6, 182, 212, 0.2);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--text-primary), var(--accent-cyan));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 12px 0;
    }
    
    .metric-value-blue {
        background: linear-gradient(135deg, var(--text-primary), var(--accent-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-value-purple {
        background: linear-gradient(135deg, var(--text-primary), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-value-pink {
        background: linear-gradient(135deg, var(--text-primary), var(--accent-pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-value-green {
        background: linear-gradient(135deg, var(--text-primary), var(--accent-green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-value-orange {
        background: linear-gradient(135deg, var(--text-primary), var(--accent-orange));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-delta-positive {
        color: var(--accent-green);
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .metric-delta-negative {
        color: var(--accent-red);
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    /* ===== FEATURE CARDS - UNIFORM SIZE ===== */
    .feature-card {
        background: linear-gradient(145deg, #16161f 0%, #1a1a24 100%);
        border-radius: 20px;
        padding: 35px 25px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        min-height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-12px) scale(1.02);
        border-color: transparent;
        box-shadow: 0 20px 50px rgba(6, 182, 212, 0.15);
    }
    
    .feature-card:hover::after {
        opacity: 1;
    }
    
    .feature-card-cyan:hover {
        box-shadow: 0 20px 50px rgba(6, 182, 212, 0.2);
        border-color: var(--accent-cyan);
    }
    
    .feature-card-blue:hover {
        box-shadow: 0 20px 50px rgba(59, 130, 246, 0.2);
        border-color: var(--accent-blue);
    }
    
    .feature-card-purple:hover {
        box-shadow: 0 20px 50px rgba(139, 92, 246, 0.2);
        border-color: var(--accent-purple);
    }
    
    .feature-card-pink:hover {
        box-shadow: 0 20px 50px rgba(236, 72, 153, 0.2);
        border-color: var(--accent-pink);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 20px;
        animation: float 3s ease-in-out infinite;
    }
    
    .feature-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 10px;
    }
    
    .feature-title-cyan {
        color: var(--accent-cyan);
    }
    
    .feature-title-blue {
        color: var(--accent-blue);
    }
    
    .feature-title-purple {
        color: var(--accent-purple);
    }
    
    .feature-title-pink {
        color: var(--accent-pink);
    }
    
    .feature-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* ===== INFO/SUCCESS/WARNING/ERROR CARDS ===== */
    .info-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border-radius: 12px;
        padding: 20px 25px;
        border-left: 4px solid var(--accent-cyan);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.15);
    }
    
    .success-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(20, 184, 166, 0.1) 100%);
        border-radius: 12px;
        padding: 20px 25px;
        border-left: 4px solid var(--accent-green);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .success-card:hover {
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
    }
    
    .warning-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(251, 146, 60, 0.1) 100%);
        border-radius: 12px;
        padding: 20px 25px;
        border-left: 4px solid var(--accent-orange);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .warning-card:hover {
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.15);
    }
    
    .error-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        border-radius: 12px;
        padding: 20px 25px;
        border-left: 4px solid var(--accent-red);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .error-card:hover {
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15);
    }
    
    /* ===== TABS WITH HOVER EFFECT ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, #16161f 0%, #1a1a24 100%);
        border-radius: 12px;
        color: var(--text-secondary);
        padding: 12px 24px;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(145deg, #1e1e2d 0%, #252532 100%);
        border-color: var(--accent-cyan);
        color: var(--accent-cyan);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 100%) !important;
        color: white !important;
        border: none;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4);
        transform: translateY(-3px);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* ===== DATAFRAME ===== */
    .dataframe {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }
    
    /* ===== FOOTER ===== */
    .footer {
        background: linear-gradient(135deg, #0f0f18 0%, #12121a 100%);
        padding: 30px;
        text-align: center;
        border-top: 1px solid var(--border-color);
        margin-top: 60px;
        border-radius: 20px 20px 0 0;
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple), var(--accent-pink));
    }
    
    .footer-title {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .footer-subtitle {
        color: var(--text-muted);
        font-size: 0.9rem;
        margin-bottom: 12px;
    }
    
    .footer-names {
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 1.05rem;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 30px 0;
    }
    
    /* ===== SLIDER ===== */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue)) !important;
    }
    
    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border-color: var(--border-color);
        border-radius: 10px;
    }
    
    /* ===== NUMBER INPUT ===== */
    .stNumberInput > div > div > input {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border-color: var(--border-color);
        border-radius: 10px;
    }
    
    /* ===== STATS CONTAINER ===== */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 20px 0;
    }
    
    /* ===== GLOW TEXT ===== */
    .glow-cyan {
        color: var(--accent-cyan);
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
    }
    
    .glow-blue {
        color: var(--accent-blue);
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
    }
    
    .glow-purple {
        color: var(--accent-purple);
        text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
    }
    
    /* ===== ANIMATED BORDER ===== */
    .animated-border {
        border: 2px solid transparent;
        background: linear-gradient(var(--bg-card), var(--bg-card)) padding-box,
                    linear-gradient(135deg, var(--accent-cyan), var(--accent-purple), var(--accent-pink)) border-box;
        animation: borderGlow 4s ease infinite;
    }
    
    /* ===== GLASS EFFECT ===== */
    .glass-card {
        background: rgba(22, 22, 31, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
    }
    
</style>
""", unsafe_allow_html=True)
# ============================================================================
# HELPER FUNCTIONS FOR UI
# ============================================================================

def create_metric_card(label, value, delta=None, delta_type="positive", color="cyan"):
    """Create a styled metric card with hover effect and uniform size."""
    delta_html = ""
    if delta:
        delta_class = "metric-delta-positive" if delta_type == "positive" else "metric-delta-negative"
        delta_icon = "↑" if delta_type == "positive" else "↓"
        delta_html = f'<div class="{delta_class}">{delta_icon} {delta}</div>'
    
    value_class = f"metric-value metric-value-{color}"
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="{value_class}">{value}</div>
        {delta_html}
    </div>
    """

def create_feature_card(icon, title, description, color="cyan"):
    """Create a feature card with hover effect and uniform size."""
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

def show_footer():
    """Display the footer with team names."""
    st.markdown("""
    <div class="footer">
        <div class="footer-title">🚀 UAE Pulse Simulator + Data Rescue Dashboard</div>
        <div class="footer-subtitle">Built with ❤️ by</div>
        <div class="footer-names">Kartik Joshi • Gagandeep Singh • Samuel Alex • Prem Kukreja</div>
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
    <div style="text-align: center; padding: 25px 0;">
        <div style="font-size: 3rem; margin-bottom: 10px;">🚀</div>
        <h1 style="
            background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.6rem; 
            margin-bottom: 5px;
            font-weight: 700;
        ">UAE Pulse</h1>
        <p style="color: #64748b; font-size: 0.85rem;">Simulator + Data Rescue</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown('<p style="color: #06b6d4; font-weight: 600; margin-bottom: 15px; letter-spacing: 1px;">📍 NAVIGATION</p>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📂 Data", "🧹 Cleaner", "🎯 Simulator", "📊 Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Data Status
    st.markdown('<p style="color: #3b82f6; font-weight: 600; margin-bottom: 15px; letter-spacing: 1px;">📡 STATUS</p>', unsafe_allow_html=True)
    
    data_loaded = st.session_state.data_loaded
    data_cleaned = st.session_state.is_cleaned
    
    status_color_loaded = "#10b981" if data_loaded else "#ef4444"
    status_color_cleaned = "#10b981" if data_cleaned else "#f59e0b" if data_loaded else "#ef4444"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #16161f 0%, #1a1a24 100%);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #2d2d3a;
    ">
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="
                width: 12px; 
                height: 12px; 
                border-radius: 50%; 
                background: {status_color_loaded}; 
                margin-right: 12px;
                box-shadow: 0 0 10px {status_color_loaded};
            "></div>
            <span style="color: #e0e0e0; font-size: 0.9rem;">Data Loaded</span>
        </div>
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="
                width: 12px; 
                height: 12px; 
                border-radius: 50%; 
                background: {status_color_cleaned}; 
                margin-right: 12px;
                box-shadow: 0 0 10px {status_color_cleaned};
            "></div>
            <span style="color: #e0e0e0; font-size: 0.9rem;">Data Cleaned</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    if st.session_state.data_loaded:
        st.markdown("---")
        st.markdown('<p style="color: #8b5cf6; font-weight: 600; margin-bottom: 15px; letter-spacing: 1px;">📈 QUICK STATS</p>', unsafe_allow_html=True)
        
        sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
        if sales_df is not None:
            total_records = len(sales_df)
            total_revenue = (sales_df['qty'] * sales_df['selling_price_aed']).sum() if 'qty' in sales_df.columns else 0
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #16161f 0%, #1a1a24 100%);
                border-radius: 12px;
                padding: 15px;
                border: 1px solid #2d2d3a;
            ">
                <div style="margin-bottom: 12px;">
                    <span style="color: #64748b; font-size: 0.8rem;">RECORDS</span><br>
                    <span style="color: #06b6d4; font-weight: 700; font-size: 1.3rem;">{total_records:,}</span>
                </div>
                <div>
                    <span style="color: #64748b; font-size: 0.8rem;">REVENUE</span><br>
                    <span style="color: #10b981; font-weight: 700; font-size: 1.1rem;">AED {total_revenue:,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PAGE: HOME
# ============================================================================

def show_home_page():
    """Display the enhanced home page."""
    
    if not st.session_state.data_loaded:
        # ===== HERO SECTION =====
        st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">✨ UAE E-Commerce Analytics</div>
            <div class="hero-badge" style="background: linear-gradient(135deg, #8b5cf6, #ec4899);">🚀 v2.0</div>
            <h1 class="hero-title">UAE Pulse Simulator</h1>
            <p class="hero-subtitle">
                Transform your e-commerce data into actionable insights. Clean dirty data, 
                simulate promotional campaigns, and visualize performance metrics.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== FEATURE CARDS =====
        st.markdown("### ✨ Powerful Features")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_feature_card(
                "📂", "Data Upload", 
                "Upload and preview your e-commerce CSV files with instant validation",
                "cyan"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_feature_card(
                "🧹", "Data Rescue", 
                "Detect & auto-fix 15+ types of data quality issues",
                "blue"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_feature_card(
                "🎯", "Simulator", 
                "Run what-if scenarios and forecast campaign ROI",
                "purple"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_feature_card(
                "📊", "Analytics", 
                "Interactive dashboards with real-time KPI tracking",
                "pink"
            ), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ===== CAPABILITIES SECTION =====
        st.markdown("### 🔥 What You Can Do")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4 style="color: #06b6d4; margin-top: 0;">🧹 Data Cleaning Capabilities</h4>
                <ul style="color: #94a3b8; margin-bottom: 0;">
                    <li>Missing value detection & imputation</li>
                    <li>Duplicate record removal</li>
                    <li>Outlier detection & capping</li>
                    <li>Format standardization</li>
                    <li>Foreign key validation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-card" style="border-left-color: #8b5cf6;">
                <h4 style="color: #8b5cf6; margin-top: 0;">🎯 Simulation Features</h4>
                <ul style="color: #94a3b8; margin-bottom: 0;">
                    <li>Discount impact modeling</li>
                    <li>Category elasticity analysis</li>
                    <li>Channel performance comparison</li>
                    <li>ROI & margin forecasting</li>
                    <li>Risk warning system</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ===== GET STARTED BUTTON =====
        st.markdown("### 🚀 Ready to Start?")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📥 Load Sample Data & Explore", use_container_width=True):
                with st.spinner("🔄 Loading sample data..."):
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
        # ===== DATA LOADED - SHOW KPI DASHBOARD =====
        sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
        products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
        stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
        
        # Header
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="
                background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5rem;
                margin-bottom: 10px;
            ">📊 Performance Dashboard</h1>
            <p style="color: #64748b; font-size: 1rem;">Real-time insights from your e-commerce data</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize simulator
        sim = Simulator()
        
        # Calculate KPIs
        kpis = sim.calculate_overall_kpis(sales_df, products_df)
        
        # ===== KPI CARDS ROW 1 =====
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Total Revenue", 
                f"AED {kpis['total_revenue']:,.0f}",
                color="cyan"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Total Orders", 
                f"{kpis['total_orders']:,}",
                color="blue"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Avg Order Value", 
                f"AED {kpis['avg_order_value']:,.2f}",
                color="purple"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Profit Margin", 
                f"{kpis['profit_margin_pct']:.1f}%",
                color="green"
            ), unsafe_allow_html=True)
        
        # ===== KPI CARDS ROW 2 =====
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Total Profit", 
                f"AED {kpis['total_profit']:,.0f}",
                color="green"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Total Units", 
                f"{kpis['total_units']:,}",
                color="orange"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Return Rate", 
                f"{kpis['return_rate_pct']:.1f}%",
                color="pink"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Avg Discount", 
                f"{kpis['avg_discount_pct']:.1f}%",
                color="blue"
            ), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== CHARTS =====
        st.markdown("### 📈 Quick Overview")
        
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
                    color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6'],
                    hole=0.45
                )
                fig = style_plotly_chart(fig)
                fig.update_traces(textposition='outside', textinfo='percent+label', textfont_size=14)
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
                    color_discrete_sequence=['#10b981', '#f59e0b', '#ec4899']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # ===== STATUS CARDS =====
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.is_cleaned:
                st.markdown(create_success_card("Data has been cleaned and validated. Ready for simulation!"), unsafe_allow_html=True)
            else:
                st.markdown(create_warning_card("Data not yet cleaned. Go to 🧹 Cleaner to validate and fix issues."), unsafe_allow_html=True)
        
        with col2:
            source = "Cleaned Data ✨" if st.session_state.is_cleaned else "Raw Data 📥"
            st.markdown(create_info_card(f"<strong>Data Source:</strong> {source}"), unsafe_allow_html=True)
    
    show_footer()
    # ============================================================================
# PAGE: DATA
# ============================================================================

def show_data_page():
    """Display the data management page."""
    
    st.markdown("""
    <h1 style="
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">📂 Data Management</h1>
    """, unsafe_allow_html=True)
    st.markdown("Upload, view, and manage your e-commerce data files.")
    
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
                df = st.session_state.raw_products
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(create_metric_card("Rows", f"{len(df):,}", color="cyan"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_metric_card("Columns", f"{len(df.columns)}", color="blue"), unsafe_allow_html=True)
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
                    st.markdown(create_metric_card("Null %", f"{null_pct:.1f}%", color="orange"), unsafe_allow_html=True)
                st.dataframe(df.head(100), use_container_width=True)
        
        with tab2:
            if st.session_state.raw_stores is not None:
                df = st.session_state.raw_stores
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(create_metric_card("Rows", f"{len(df):,}", color="cyan"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_metric_card("Columns", f"{len(df.columns)}", color="blue"), unsafe_allow_html=True)
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
                    st.markdown(create_metric_card("Null %", f"{null_pct:.1f}%", color="orange"), unsafe_allow_html=True)
                st.dataframe(df.head(100), use_container_width=True)
        
        with tab3:
            if st.session_state.raw_sales is not None:
                df = st.session_state.raw_sales
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(create_metric_card("Rows", f"{len(df):,}", color="cyan"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_metric_card("Columns", f"{len(df.columns)}", color="blue"), unsafe_allow_html=True)
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
                    st.markdown(create_metric_card("Null %", f"{null_pct:.1f}%", color="orange"), unsafe_allow_html=True)
                st.dataframe(df.head(100), use_container_width=True)
        
        with tab4:
            if st.session_state.raw_inventory is not None:
                df = st.session_state.raw_inventory
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(create_metric_card("Rows", f"{len(df):,}", color="cyan"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_metric_card("Columns", f"{len(df.columns)}", color="blue"), unsafe_allow_html=True)
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
                    st.markdown(create_metric_card("Null %", f"{null_pct:.1f}%", color="orange"), unsafe_allow_html=True)
                st.dataframe(df.head(100), use_container_width=True)
    
    show_footer()

# ============================================================================
# PAGE: CLEANER
# ============================================================================

def show_cleaner_page():
    """Display the data cleaner page."""
    
    st.markdown("""
    <h1 style="
        background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">🧹 Data Rescue Center</h1>
    """, unsafe_allow_html=True)
    st.markdown("Validate, detect issues, and clean your dirty data automatically.")
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    # Issue types info
    st.markdown("### 🔍 Issues We Detect & Fix")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <strong style="color: #06b6d4;">Data Quality</strong>
            <ul style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0;">
                <li>Missing values</li>
                <li>Null representations</li>
                <li>Duplicate records</li>
                <li>Whitespace issues</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="border-left-color: #8b5cf6;">
            <strong style="color: #8b5cf6;">Format Issues</strong>
            <ul style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0;">
                <li>Invalid timestamps</li>
                <li>Mixed case values</li>
                <li>Boolean strings</li>
                <li>Invalid categories</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card" style="border-left-color: #ec4899;">
            <strong style="color: #ec4899;">Value Issues</strong>
            <ul style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0;">
                <li>Negative values</li>
                <li>Outliers</li>
                <li>FK violations</li>
                <li>Invalid references</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clean data button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Data Cleaning", use_container_width=True, type="primary"):
            with st.spinner("🔄 Analyzing and cleaning data... This may take a moment."):
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
            delta = f"{before - after} removed" if before > after else "No change"
            delta_type = "negative" if before > after else "positive"
            st.markdown(create_metric_card("Products", f"{after:,}", delta, delta_type, "cyan"), unsafe_allow_html=True)
        
        with col2:
            before = stats['stores']['before']
            after = stats['stores']['after']
            delta = f"{before - after} removed" if before > after else "No change"
            delta_type = "negative" if before > after else "positive"
            st.markdown(create_metric_card("Stores", f"{after:,}", delta, delta_type, "blue"), unsafe_allow_html=True)
        
        with col3:
            before = stats['sales']['before']
            after = stats['sales']['after']
            delta = f"{before - after} removed" if before > after else "No change"
            delta_type = "negative" if before > after else "positive"
            st.markdown(create_metric_card("Sales", f"{after:,}", delta, delta_type, "purple"), unsafe_allow_html=True)
        
        with col4:
            before = stats['inventory']['before']
            after = stats['inventory']['after']
            delta = f"{before - after} removed" if before > after else "No change"
            delta_type = "negative" if before > after else "positive"
            st.markdown(create_metric_card("Inventory", f"{after:,}", delta, delta_type, "pink"), unsafe_allow_html=True)
        
        # Issues summary
        st.markdown("---")
        st.markdown("### 🔍 Issues Detected & Fixed")
        
        issues_df = st.session_state.issues_df
        
        if len(issues_df) > 0:
            # Total issues card
            st.markdown(create_success_card(f"Total {len(issues_df)} issues detected and fixed automatically!"), unsafe_allow_html=True)
            
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
                    color_continuous_scale=['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(coloraxis_showscale=False)
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
                    color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899'],
                    hole=0.45
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            # Issues table
            st.markdown("### 📋 Detailed Issues Log")
            st.dataframe(issues_df, use_container_width=True)
            
            # Download button
            csv = issues_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Issues Log (CSV)",
                data=csv,
                file_name="data_issues_log.csv",
                mime="text/csv"
            )
        else:
            st.markdown(create_success_card("No issues found! Your data is already clean."), unsafe_allow_html=True)
    
    show_footer()

# ============================================================================
# PAGE: SIMULATOR
# ============================================================================

def show_simulator_page():
    """Display the campaign simulator page."""
    
    st.markdown("""
    <h1 style="
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">🎯 Campaign Simulator</h1>
    """, unsafe_allow_html=True)
    st.markdown("Run what-if scenarios and forecast campaign outcomes with precision.")
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    if not st.session_state.is_cleaned:
        st.markdown(create_warning_card("Please clean data first. Go to 🧹 Cleaner page for better results."), unsafe_allow_html=True)
    
    # Campaign parameters
    st.markdown("### ⚙️ Campaign Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<p style="color: #06b6d4; font-weight: 600; margin-bottom: 10px;">💰 Pricing</p>', unsafe_allow_html=True)
        discount_pct = st.slider("Discount %", 0, 50, 15, help="Discount percentage to offer")
        promo_budget = st.number_input("Promo Budget (AED)", 1000, 500000, 25000, step=5000)
    
    with col2:
        st.markdown('<p style="color: #8b5cf6; font-weight: 600; margin-bottom: 10px;">📊 Constraints</p>', unsafe_allow_html=True)
        margin_floor = st.slider("Margin Floor %", 0, 50, 15, help="Minimum acceptable profit margin")
        campaign_days = st.slider("Campaign Days", 1, 30, 7)
    
    with col3:
        st.markdown('<p style="color: #ec4899; font-weight: 600; margin-bottom: 10px;">🎯 Targeting</p>', unsafe_allow_html=True)
        city = st.selectbox("Target City", ['All', 'Dubai', 'Abu Dhabi', 'Sharjah'])
        channel = st.selectbox("Target Channel", ['All', 'App', 'Web', 'Marketplace'])
        category = st.selectbox("Target Category", ['All', 'Electronics', 'Fashion', 'Grocery', 'Beauty', 'Home', 'Sports'])
    
    st.markdown("---")
    
    # Run simulation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_sim = st.button("🚀 Run Simulation", use_container_width=True, type="primary")
    
    if run_sim:
        with st.spinner("🔄 Running simulation..."):
            sim = Simulator()
            
            sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
            stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
            products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
            
            results = sim.simulate_campaign(
                sales_df, stores_df, products_df,
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
            
            # Row 1
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                delta = f"{comparison['revenue_change_pct']:+.1f}%"
                delta_type = "positive" if comparison['revenue_change_pct'] > 0 else "negative"
                st.markdown(create_metric_card("Expected Revenue", f"AED {outputs['expected_revenue']:,.0f}", delta, delta_type, "cyan"), unsafe_allow_html=True)
            
            with col2:
                delta = f"{comparison['order_change_pct']:+.1f}%"
                delta_type = "positive" if comparison['order_change_pct'] > 0 else "negative"
                st.markdown(create_metric_card("Expected Orders", f"{outputs['expected_orders']:,}", delta, delta_type, "blue"), unsafe_allow_html=True)
            
            with col3:
                delta = f"{comparison['profit_change_pct']:+.1f}%"
                delta_type = "positive" if comparison['profit_change_pct'] > 0 else "negative"
                st.markdown(create_metric_card("Net Profit", f"AED {outputs['expected_net_profit']:,.0f}", delta, delta_type, "green"), unsafe_allow_html=True)
            
            with col4:
                color = "green" if outputs['roi_pct'] > 0 else "pink"
                st.markdown(create_metric_card("ROI", f"{outputs['roi_pct']:.1f}%", color=color), unsafe_allow_html=True)
            
            # Row 2
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card("Demand Lift", f"+{outputs['demand_lift_pct']:.1f}%", color="purple"), unsafe_allow_html=True)
            
            with col2:
                color = "green" if outputs['expected_margin_pct'] >= margin_floor else "orange"
                st.markdown(create_metric_card("Margin", f"{outputs['expected_margin_pct']:.1f}%", color=color), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card("Promo Cost", f"AED {outputs['promo_cost']:,.0f}", color="orange"), unsafe_allow_html=True)
            
            with col4:
                st.markdown(create_metric_card("Fulfillment", f"AED {outputs['fulfillment_cost']:,.0f}", color="blue"), unsafe_allow_html=True)
            
            # Warnings
            if warnings:
                st.markdown("---")
                st.markdown("### ⚠️ Risk Alerts")
                for warning in warnings:
                    st.markdown(create_warning_card(warning), unsafe_allow_html=True)
            else:
                st.markdown("---")
                st.markdown(create_success_card("All metrics within acceptable range. Campaign looks healthy!"), unsafe_allow_html=True)
            
            # Comparison chart
            st.markdown("---")
            st.markdown("### 📈 Baseline vs Campaign Comparison")
            
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
                fig.update_layout(barmode='group', title='Revenue & Profit Comparison')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Orders comparison
                orders_data = pd.DataFrame({
                    'Type': ['Baseline', 'Campaign'],
                    'Orders': [comparison['baseline_orders'], outputs['expected_orders']]
                })
                
                fig = px.bar(
                    orders_data,
                    x='Type',
                    y='Orders',
                    title='Orders Comparison',
                    color='Type',
                    color_discrete_sequence=['#8b5cf6', '#ec4899']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    show_footer()

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================

def show_analytics_page():
    """Display the analytics page."""
    
    st.markdown("""
    <h1 style="
        background: linear-gradient(135deg, #f59e0b 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">📊 Analytics Dashboard</h1>
    """, unsafe_allow_html=True)
    st.markdown("Deep dive into your e-commerce performance metrics and trends.")
    
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
        st.markdown("### 📈 Daily Performance Trends")
        daily_trends = sim.calculate_daily_trends(sales_df, products_df)
        
        if len(daily_trends) > 0:
            # Main revenue chart
            fig = px.area(
                daily_trends,
                x='date',
                y='revenue',
                title='Daily Revenue Trend',
                color_discrete_sequence=['#06b6d4']
            )
            fig = style_plotly_chart(fig)
            fig.update_traces(line=dict(width=3), fillcolor='rgba(6, 182, 212, 0.2)')
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
                fig.update_traces(line=dict(width=3))
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
                fig.update_traces(line=dict(width=3))
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🏙️ Performance by City")
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
                    color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    city_kpis,
                    x='city',
                    y='profit_margin_pct',
                    title='Profit Margin by City',
                    color='city',
                    color_discrete_sequence=['#10b981', '#14b8a6', '#06b6d4']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 📋 City Performance Table")
            st.dataframe(city_kpis, use_container_width=True)
    
    with tab3:
        st.markdown("### 📦 Performance by Category")
        cat_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'category')
        
        if len(cat_kpis) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    cat_kpis,
                    values='revenue',
                    names='category',
                    title='Revenue Share by Category',
                    color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'],
                    hole=0.45
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    cat_kpis,
                    x='category',
                    y='profit',
                    title='Profit by Category',
                    color='profit',
                    color_continuous_scale=['#3b82f6', '#8b5cf6', '#ec4899']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 📋 Category Performance Table")
            st.dataframe(cat_kpis, use_container_width=True)
    
    with tab4:
        st.markdown("### 📋 Inventory Health")
        stockout = sim.calculate_stockout_risk(inventory_df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_metric_card("Total SKUs", f"{stockout['total_items']:,}", color="cyan"), unsafe_allow_html=True)
        
        with col2:
            color = "orange" if stockout['stockout_risk_pct'] > 10 else "green"
            st.markdown(create_metric_card("Stockout Risk", f"{stockout['stockout_risk_pct']:.1f}%", color=color), unsafe_allow_html=True)
        
        with col3:
            color = "pink" if stockout['zero_stock'] > 0 else "green"
            st.markdown(create_metric_card("Zero Stock", f"{stockout['zero_stock']:,}", color=color), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Inventory distribution
        if inventory_df is not None and 'stock_on_hand' in inventory_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    inventory_df,
                    x='stock_on_hand',
                    nbins=50,
                    title='Stock Level Distribution',
                    color_discrete_sequence=['#8b5cf6']
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Stock status pie
                inventory_df_copy = inventory_df.copy()
                inventory_df_copy['status'] = inventory_df_copy.apply(
                    lambda x: 'Critical' if x['stock_on_hand'] == 0 
                    else ('Low' if x['stock_on_hand'] <= x.get('reorder_point', 10) else 'Healthy'),
                    axis=1
                )
                status_counts = inventory_df_copy['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                
                fig = px.pie(
                    status_counts,
                    values='Count',
                    names='Status',
                    title='Inventory Status',
                    color='Status',
                    color_discrete_map={'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'},
                    hole=0.45
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
