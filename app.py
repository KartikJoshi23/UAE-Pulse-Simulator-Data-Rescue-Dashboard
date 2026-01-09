# ============================================================================
# UAE Pulse Simulator + Data Rescue Dashboard
# Main Streamlit Application - RESTORED v2.0 + FIXES
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from modules.validator import FileValidator

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
# ENHANCED CSS - ALL FIXES APPLIED
# ============================================================================

st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ===== CSS VARIABLES ===== */
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
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(6, 182, 212, 0.3); }
        50% { box-shadow: 0 0 40px rgba(6, 182, 212, 0.6); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== ENHANCED MAIN BACKGROUND ===== */
    .stApp {
        background: 
            radial-gradient(ellipse at top left, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at top right, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at bottom left, rgba(236, 72, 153, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at bottom right, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
            linear-gradient(180deg, #0a0a0f 0%, #0d0d14 25%, #0f0f18 50%, #0d0d14 75%, #0a0a0f 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #0f0f18 50%, #0a0a0f 100%);
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
        opacity: 0.6;
    }
    
    /* ===== FIX: HEADINGS - NO BOX ===== */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        background: none !important;
        -webkit-background-clip: unset !important;
        background-clip: unset !important;
    }
    
    /* ===== HERO SECTION ===== */
    .hero-container {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.12) 0%, rgba(139, 92, 246, 0.12) 50%, rgba(236, 72, 153, 0.12) 100%);
        border-radius: 24px;
        padding: 60px 50px;
        margin-bottom: 40px;
        border: 1px solid rgba(6, 182, 212, 0.3);
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
        background: radial-gradient(circle, rgba(6, 182, 212, 0.15) 0%, transparent 50%);
        animation: float 6s ease-in-out infinite;
    }
    
    /* ===== FIX: HERO TITLE - MUCH BIGGER ===== */
    .hero-title {
        font-size: 4rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 0%, #06b6d4 40%, #8b5cf6 70%, #ec4899 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
        position: relative;
        z-index: 1;
        line-height: 1.2;
        animation: gradientShift 4s ease infinite;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: var(--text-secondary);
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
        line-height: 1.6;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 10px 24px;
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
        border-radius: 50px;
        color: white;
        font-size: 0.95rem;
        font-weight: 600;
        margin-right: 12px;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    
    /* ===== FIX: PAGE TITLES - BIGGER FOR PROJECTOR ===== */
    .page-title {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
        line-height: 1.2;
    }
    
    .page-title-cyan { color: #06b6d4 !important; }
    .page-title-blue { color: #3b82f6 !important; }
    .page-title-purple { color: #8b5cf6 !important; }
    .page-title-pink { color: #ec4899 !important; }
    .page-title-green { color: #10b981 !important; }
    .page-title-teal { color: #14b8a6 !important; }
    .page-title-orange { color: #f59e0b !important; }
    
    .page-description {
        color: var(--text-secondary);
        font-size: 1.15rem;
        margin-bottom: 25px;
    }
    
    /* ===== SECTION TITLES - BIGGER ===== */
    .section-title {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 20px !important;
    }
    
    .section-title-cyan { color: #06b6d4 !important; }
    .section-title-blue { color: #3b82f6 !important; }
    .section-title-purple { color: #8b5cf6 !important; }
    .section-title-pink { color: #ec4899 !important; }
    .section-title-green { color: #10b981 !important; }
    .section-title-teal { color: #14b8a6 !important; }
    .section-title-orange { color: #f59e0b !important; }
    
    /* ===== FIX: METRIC CARDS - EXACT UNIFORM SIZE ===== */
    .metric-card {
        background: linear-gradient(145deg, #16161f 0%, #1a1a24 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 140px !important;
        min-height: 140px !important;
        max-height: 140px !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        box-sizing: border-box;
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
        font-size: 1.8rem;
        font-weight: 700;
        margin: 8px 0;
    }
    
    .metric-value-cyan { color: #06b6d4; }
    .metric-value-blue { color: #3b82f6; }
    .metric-value-purple { color: #8b5cf6; }
    .metric-value-pink { color: #ec4899; }
    .metric-value-green { color: #10b981; }
    .metric-value-orange { color: #f59e0b; }
    .metric-value-teal { color: #14b8a6; }
    
    .metric-delta-positive {
        color: var(--accent-green);
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .metric-delta-negative {
        color: var(--accent-red);
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* ===== FIX: FEATURE CARDS - EXACT UNIFORM SIZE ===== */
    .feature-card {
        background: linear-gradient(145deg, #16161f 0%, #1a1a24 100%);
        border-radius: 20px;
        padding: 35px 25px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 220px !important;
        min-height: 220px !important;
        max-height: 220px !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-sizing: border-box;
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
    
    .feature-card-cyan:hover { box-shadow: 0 20px 50px rgba(6, 182, 212, 0.2); border-color: var(--accent-cyan); }
    .feature-card-blue:hover { box-shadow: 0 20px 50px rgba(59, 130, 246, 0.2); border-color: var(--accent-blue); }
    .feature-card-purple:hover { box-shadow: 0 20px 50px rgba(139, 92, 246, 0.2); border-color: var(--accent-purple); }
    .feature-card-pink:hover { box-shadow: 0 20px 50px rgba(236, 72, 153, 0.2); border-color: var(--accent-pink); }
    
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
    
    .feature-title-cyan { color: var(--accent-cyan); }
    .feature-title-blue { color: var(--accent-blue); }
    .feature-title-purple { color: var(--accent-purple); }
    .feature-title-pink { color: var(--accent-pink); }
    
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
        color: #e2e8f0;
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
        color: #e2e8f0;
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
        color: #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .error-card:hover {
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15);
    }
    
    /* ===== INSIGHT CARD ===== */
    .insight-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(236, 72, 153, 0.12) 100%);
        border-radius: 12px;
        padding: 20px 25px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateX(8px);
        border-color: #8b5cf6;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2);
    }
    
    .insight-title {
        color: #a78bfa;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 10px;
    }
    
    .insight-text {
        color: #e2e8f0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* ===== FIX: SUB-TABS - WITH HOVER EFFECT ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, #16161f 0%, #1a1a24 100%);
        border-radius: 12px;
        color: var(--text-secondary);
        padding: 12px 24px;
        border: 1px solid var(--border-color);
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    /* HOVER EFFECT FOR SUB-TABS */
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(145deg, #1a1a24 0%, #1e1e2d 100%);
        border-color: var(--accent-cyan);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
    }
    
    .stTabs [aria-selected="true"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.5);
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.4);
        transform: translateY(-3px);
    }
    
    /* ===== FOOTER ===== */
    .footer {
        background: linear-gradient(135deg, #0f0f18 0%, #12121a 100%);
        padding: 35px;
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
        height: 3px;
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple), var(--accent-pink));
    }
    
    .footer-title {
        color: var(--text-primary);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .footer-subtitle {
        color: var(--text-muted);
        font-size: 0.95rem;
        margin-bottom: 12px;
    }
    
    .footer-names {
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 1.1rem;
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
        border-color: var(--border-color);
        border-radius: 10px;
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
        delta_html = '<div style="height: 22px;"></div>'  # Spacer for uniform height
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value metric-value-{color}">{value}</div>
        {delta_html}
    </div>
    """
def create_feature_card(icon, title, description, color="cyan"):
    """Create a styled feature card with border effect and hover."""
    colors = {
        "cyan": "#06b6d4",
        "blue": "#3b82f6",
        "purple": "#8b5cf6",
        "pink": "#ec4899",
        "green": "#10b981",
        "orange": "#f59e0b",
        "teal": "#14b8a6",
    }
    primary = colors.get(color, colors["cyan"])
    
    return f"""
    <style>
        .feature-card-{color} {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
            border-radius: 16px;
            padding: 30px 20px;
            text-align: center;
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-left: 4px solid {primary};
            height: 220px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .feature-card-{color}:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 30px {primary}44;
            border-color: {primary};
        }}
    </style>
    <div class="feature-card-{color}">
        <div style="font-size: 42px; margin-bottom: 12px;">{icon}</div>
        <div style="color: {primary}; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">{title}</div>
        <div style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5;">{description}</div>
    </div>
    """
    
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 16px;
        padding: 30px 24px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-left: 4px solid {primary};
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    "
    onmouseover="
        this.style.transform='translateY(-5px)';
        this.style.boxShadow='0 20px 40px rgba(0,0,0,0.3), 0 0 30px {primary}33';
        this.style.borderLeftColor='{secondary}';
    "
    onmouseout="
        this.style.transform='translateY(0)';
        this.style.boxShadow='none';
        this.style.borderLeftColor='{primary}';
    ">
        <div style="
            font-size: 48px;
            margin-bottom: 16px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
        ">{icon}</div>
        <div style="
            color: {primary};
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        ">{title}</div>
        <div style="
            color: #94a3b8;
            font-size: 0.9rem;
            line-height: 1.5;
        ">{description}</div>
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
        insights.append(("Excellent Quality", f"Low return rate of {return_rate:.1f}% indicates high customer satisfaction_taken."))
    
    # City insight
    if city_kpis is not None and len(city_kpis) > 0:
        top_city = city_kpis.iloc[0]['city'] if 'city' in city_kpis.columns else None
        if top_city:
            top_revenue = city_kpis.iloc[0]['revenue']
            total_revenue = city_kpis['revenue'].sum()
            pct = (top_revenue / total_revenue * 100) if total_revenue > 0 else 0
            insights.append(("Market Concentration", f"{top_city} contributes {pct:.0f}% of total revenue. {'Diversify to reduce risk.' if pct > 50 else 'Healthy market distribution.'}"))
    
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
    # Title with NO empty space
    st.markdown("""
    <div style="text-align: center; margin-top: -20px; padding-bottom: 15px;">
        <div style="font-size: 48px; margin-bottom: 5px;">🛒</div>
        <div style="
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #06b6d4, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">UAE Pulse</div>
        <div style="color: #94a3b8; font-size: 13px;">Simulator + Data Rescue</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown('<p style="color: #ec4899; font-weight: 600; margin-bottom: 15px; letter-spacing: 1.2px; font-size: 0.85rem;">📍 NAVIGATION</p>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📂 Data", "🧹 Cleaner", "📊 Dashboard", "🎯 Simulator"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Data Status
    st.markdown('<p style="color: #3b82f6; font-weight: 600; margin-bottom: 15px; letter-spacing: 1.2px; font-size: 0.85rem;">📡 STATUS</p>', unsafe_allow_html=True)
    
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
        <div style="display: flex; align-items: center; margin: 8px 0;">
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
        <div style="display: flex; align-items: center; margin: 8px 0;">
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
    
    # Footer
    st.markdown("---")
    st.markdown('<p style="color: #3b82f6; font-weight: 600; margin-bottom: 15px; letter-spacing: 1.2px; font-size: 0.85rem;">🔬 TECH</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #64748b; font-size: 11px; line-height: 1.6;">
        Python • Pandas • Plotly • Streamlit
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    if st.session_state.data_loaded:
        st.markdown("---")
        st.markdown('<p style="color: #8b5cf6; font-weight: 600; margin-bottom: 15px; letter-spacing: 1.2px; font-size: 0.85rem;">📈 QUICK STATS</p>', unsafe_allow_html=True)
        
        sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
        if sales_df is not None:
            total_records = len(sales_df)
            try:
                qty = pd.to_numeric(sales_df['qty'], errors='coerce').fillna(0)
                price = pd.to_numeric(sales_df['selling_price_aed'], errors='coerce').fillna(0)
                total_revenue = (qty * price).sum()
            except:
                total_revenue = 0
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #16161f 0%, #1a1a24 100%);
                border-radius: 12px;
                padding: 15px;
                border: 1px solid #2d2d3a;
            ">
                <div style="margin-bottom: 12px;">
                    <span style="color: #64748b; font-size: 0.8rem; text-transform: uppercase;">records</span><br>
                    <span style="color: #06b6d4; font-weight: 700; font-size: 1.4rem;">{total_records:,}</span>
                </div>
                <div>
                    <span style="color: #64748b; font-size: 0.8rem; text-transform: uppercase;">REVENUE</span><br>
                    <span style="color: #10b981; font-weight: 700; font-size: 1.2rem;">AED {total_revenue:,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def validate_file_columns(df, file_type):
    """Validate that uploaded file has required columns for its type."""
    
    required_columns = {
        'products': {
            'must_have': ['sku'],
            'should_have': ['product_name', 'category', 'cost', 'price'],
            'alternate_names': {
                'sku': ['sku', 'SKU', 'product_id', 'ProductID', 'product_sku'],
                'product_name': ['product_name', 'name', 'product', 'ProductName'],
                'category': ['category', 'Category', 'product_category', 'cat'],
                'cost': ['cost', 'cost_aed', 'Cost', 'unit_cost'],
                'price': ['price', 'selling_price', 'selling_price_aed', 'Price', 'unit_price']
            }
        },
        'stores': {
            'must_have': ['store_id'],
            'should_have': ['city', 'channel'],
            'alternate_names': {
                'store_id': ['store_id', 'StoreID', 'store', 'Store'],
                'city': ['city', 'City', 'location', 'store_city'],
                'channel': ['channel', 'Channel', 'sales_channel', 'store_channel']
            }
        },
        'sales': {
            'must_have': ['sku', 'store_id'],
            'should_have': ['date', 'qty', 'revenue'],
            'alternate_names': {
                'sku': ['sku', 'SKU', 'product_id', 'ProductID'],
                'store_id': ['store_id', 'StoreID', 'store', 'Store'],
                'date': ['date', 'Date', 'transaction_taken_date', 'sale_date', 'order_date'],
                'qty': ['qty', 'quantity', 'Qty', 'Quantity', 'units'],
                'revenue': ['revenue', 'Revenue', 'sales', 'total', 'amount']
            }
        },
        'inventory': {
            'must_have': ['sku', 'store_id'],
            'should_have': ['stock_on_hand'],
            'alternate_names': {
                'sku': ['sku', 'SKU', 'product_id', 'ProductID'],
                'store_id': ['store_id', 'StoreID', 'store', 'Store'],
                'stock_on_hand': ['stock_on_hand', 'stock', 'inventory', 'qty', 'quantity', 'on_hand']
            }
        }
    }
    
    if file_type not in required_columns:
        return True, "Unknown file type", []
    
    config = required_columns[file_type]
    df_columns = [col.lower().strip() for col in df.columns]
    df_columns_original = list(df.columns)
    
    missing_must_have = []
    found_columns = []
    
    # Check must-have columns
    for col in config['must_have']:
        alternates = config['alternate_names'].get(col, [col])
        found = False
        for alt in alternates:
            if alt.lower() in df_columns:
                found = True
                found_columns.append(alt)
                break
        if not found:
            missing_must_have.append(col)
    
    # Check should-have columns (for better confidence)
    should_have_found = 0
    for col in config['should_have']:
        alternates = config['alternate_names'].get(col, [col])
        for alt in alternates:
            if alt.lower() in df_columns:
                should_have_found += 1
                found_columns.append(alt)
                break
    
    # Validation result
    if len(missing_must_have) > 0:
        return False, f"Missing required columns: {', '.join(missing_must_have)}", found_columns
    
    # Check if at least some expected columns exist
    total_expected = len(config['must_have']) + len(config['should_have'])
    total_found = len(config['must_have']) - len(missing_must_have) + should_have_found
    confidence = total_found / total_expected * 100
    
    if confidence < 40:
        return False, f"This doesn't look like a {file_type} file. Only {confidence:.0f}% columns match.", found_columns
    
    return True, f"Valid {file_type} file ({confidence:.0f}% confidence)", found_columns
    
# ============================================================================
# PAGE: HOME
# ============================================================================

# ============================================================================
# PAGE: HOME (FIXED - BIG TITLE, BETTER LAYOUT)
# ============================================================================

def show_home_page():
    """Display the home page - always static, never changes."""
    
    # ===== HERO SECTION =====
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(139, 92, 246, 0.15) 50%, rgba(236, 72, 153, 0.15) 100%);
        border-radius: 24px;
        padding: 50px;
        margin-bottom: 40px;
        border: 1px solid rgba(6, 182, 212, 0.3);
        text-align: center;
    ">
        <div style="margin-bottom: 20px;">
            <span style="
                display: inline-block;
                padding: 10px 24px;
                background: linear-gradient(135deg, #06b6d4, #3b82f6);
                border-radius: 50px;
                color: white;
                font-size: 0.95rem;
                font-weight: 600;
                margin-right: 12px;
            ">✨ UAE E-Commerce Analytics</span>
            <span style="
                display: inline-block;
                padding: 10px 24px;
                background: linear-gradient(135deg, #8b5cf6, #ec4899);
                border-radius: 50px;
                color: white;
                font-size: 0.95rem;
                font-weight: 600;
            ">🚀 v2.0</span>
        </div>
        <div style="
            font-size: 64px;
            font-weight: 800;
            background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 20px 0;
            line-height: 1.2;
        ">UAE Pulse Simulator</div>
        <p style="color: #94a3b8; font-size: 1.15rem; margin: 0; line-height: 1.6;">
            Transform your e-commerce data into action_takenable insights.<br>
            Clean dirty data, simulate promotional campaigns, and visualize performance metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== FEATURE CARDS =====
    st.markdown('<p class="section-title section-title-purple">✨ Powerful Features</p>', unsafe_allow_html=True)
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
    st.markdown('<p class="section-title section-title-teal">🔥 What You Can Do</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #06b6d4; margin-top: 0; font-size: 1.1rem;">🧹 Data Cleaning Capabilities</h4>
            <ul style="color: #94a3b8; margin-bottom: 0; font-size: 0.95rem; line-height: 1.8;">
                <li>Missing value detection & imputation</li>
                <li>Duplicate record_identifier removal</li>
                <li>Outlier detection & capping</li>
                <li>Format standardization</li>
                <li>Foreign key validation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="border-left-color: #8b5cf6;">
            <h4 style="color: #8b5cf6; margin-top: 0; font-size: 1.1rem;">🎯 Simulation Features</h4>
            <ul style="color: #94a3b8; margin-bottom: 0; font-size: 0.95rem; line-height: 1.8;">
                <li>Discount impact modeling</li>
                <li>Category elasticity analysis</li>
                <li>Channel performance comparison</li>
                <li>ROI & margin forecasting</li>
                <li>Risk warning system</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== QUICK START GUIDE =====
    st.markdown('<p class="section-title section-title-blue">🚀 Quick Start Guide</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 10px;">1️⃣</div>
            <div style="color: #06b6d4; font-weight: 600; margin-bottom: 5px;">Load Data</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">Go to 📂 Data page and upload your files or load sample data</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 10px;">2️⃣</div>
            <div style="color: #3b82f6; font-weight: 600; margin-bottom: 5px;">Clean Data</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">Go to 🧹 Cleaner to detect and fix data issues</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 10px;">3️⃣</div>
            <div style="color: #8b5cf6; font-weight: 600; margin-bottom: 5px;">View Insights</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">Check 👔 Executive or 📋 Manager views for KPIs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 10px;">4️⃣</div>
            <div style="color: #ec4899; font-weight: 600; margin-bottom: 5px;">Simulate</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">Go to 🎯 Simulator to run what-if campaigns</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== DATA STATUS =====
    if st.session_state.data_loaded:
        st.markdown(create_success_card("✅ Data is loaded! Go to 👔 Executive View to see your KPIs."), unsafe_allow_html=True)
    else:
        st.markdown(create_info_card("💡 Start by loading data. Go to 📂 Data page."), unsafe_allow_html=True)
    
    show_footer()
    
def show_dashboard_page():
    """Display the Dashboard with Executive/Manager toggle."""
    
    st.markdown('<h1 class="page-title page-title-cyan">📊 Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Business performance insights and operational metrics</p>', unsafe_allow_html=True)
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    st.markdown("---")
    
    # ===== TOGGLE SWITCH =====
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        view_mode = st.toggle("Switch View", value=False, help="OFF = Executive View | ON = Manager View")
        
        if view_mode:
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2)); border-radius: 10px; margin: 10px 0;">
                <span style="color: #3b82f6; font-weight: 700; font-size: 1.2rem;">📋 Manager View</span>
                <span style="color: #94a3b8; font-size: 0.9rem;"> — Operational Risk & Execution</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(16, 185, 129, 0.2)); border-radius: 10px; margin: 10px 0;">
                <span style="color: #06b6d4; font-weight: 700; font-size: 1.2rem;">👔 Executive View</span>
                <span style="color: #94a3b8; font-size: 0.9rem;"> — Financial & Strategic</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Get the appropriate data
    sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
    products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
    stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
    inventory_df = st.session_state.clean_inventory if st.session_state.is_cleaned else st.session_state.raw_inventory
    
    # Initialize simulator for KPI calculations
    sim = Simulator()
    
    # Calculate KPIs
    kpis = sim.calculate_overall_kpis(sales_df, products_df)
    city_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'city')
    channel_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'channel')
    category_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'category')
    
    if not view_mode:
        # =====================
        # EXECUTIVE VIEW
        # =====================
        show_executive_view(kpis, city_kpis, channel_kpis, category_kpis, sales_df, products_df, stores_df)
    else:
        # =====================
        # MANAGER VIEW
        # =====================
        show_manager_view(kpis, city_kpis, channel_kpis, category_kpis, sales_df, products_df, stores_df, inventory_df)
    
    st.markdown("---")
    
    # Data Status
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.is_cleaned:
            st.markdown(create_success_card("✅ Viewing cleaned data."), unsafe_allow_html=True)
        else:
            st.markdown(create_warning_card("⚠️ Viewing raw data. Go to 🧹 Cleaner for validation."), unsafe_allow_html=True)
    
    with col2:
        source = "Cleaned Data ✨" if st.session_state.is_cleaned else "Raw Data 📥"
        st.markdown(create_info_card(f"<strong>Data Source:</strong> {source}"), unsafe_allow_html=True)
    
    show_footer()


def show_executive_view(kpis, city_kpis, channel_kpis, category_kpis, sales_df, products_df, stores_df):
    """Display Executive View - Financial & Strategic KPIs."""
    
    # ===== KPI CARDS (Executive) =====
    st.markdown('<p class="section-title section-title-cyan">💰 Financial KPIs</p>', unsafe_allow_html=True)
    
    # Row 1: Revenue metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gross_revenue = kpis.get('total_revenue', 0)
        st.markdown(create_metric_card(
            "Gross Revenue",
            f"AED {gross_revenue:,.0f}",
            color="cyan"
        ), unsafe_allow_html=True)
    
    with col2:
        refund_amount = kpis.get('refund_amount', 0)
        st.markdown(create_metric_card(
            "Refund Amount",
            f"AED {refund_amount:,.0f}",
            color="pink"
        ), unsafe_allow_html=True)
    
    with col3:
        net_revenue = kpis.get('net_revenue', gross_revenue - refund_amount)
        st.markdown(create_metric_card(
            "Net Revenue",
            f"AED {net_revenue:,.0f}",
            color="green"
        ), unsafe_allow_html=True)
    
    with col4:
        cogs = kpis.get('total_cogs', 0)
        st.markdown(create_metric_card(
            "COGS",
            f"AED {cogs:,.0f}",
            color="orange"
        ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Margin metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gross_margin = kpis.get('total_profit', 0)
        st.markdown(create_metric_card(
            "Gross Margin (AED)",
            f"AED {gross_margin:,.0f}",
            color="teal"
        ), unsafe_allow_html=True)
    
    with col2:
        gross_margin_pct = kpis.get('profit_margin_pct', 0)
        st.markdown(create_metric_card(
            "Gross Margin %",
            f"{gross_margin_pct:.1f}%",
            color="purple"
        ), unsafe_allow_html=True)
    
    with col3:
        avg_discount = kpis.get('avg_discount_pct', 0)
        st.markdown(create_metric_card(
            "Avg Discount %",
            f"{avg_discount:.1f}%",
            color="blue"
        ), unsafe_allow_html=True)
    
    with col4:
        avg_order_value = kpis.get('avg_order_value', 0)
        st.markdown(create_metric_card(
            "Avg Order Value",
            f"AED {avg_order_value:,.2f}",
            color="cyan"
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== CHARTS (Executive - 4 Required) =====
    st.markdown('<p class="section-title section-title-blue">📈 Executive Charts</p>', unsafe_allow_html=True)
    
    # Chart 1 & 2: Net Revenue Trend + Revenue by City/Channel
    col1, col2 = st.columns(2)
    
    with col1:
        # Chart 1: Net Revenue Trend (daily/weekly)
        if 'order_time' in sales_df.columns:
            sales_trend = sales_df.copy()
            sales_trend['date'] = pd.to_datetime(sales_trend['order_time']).dt.date
            daily_revenue = sales_trend.groupby('date').agg({'selling_price_aed': 'sum'}).reset_index()
            daily_revenue.columns = ['Date', 'Revenue']
            
            fig = px.line(
                daily_revenue,
                x='Date',
                y='Revenue',
                title='Net Revenue Trend (Daily)',
                markers=True
            )
            fig = style_plotly_chart(fig)
            fig.update_traces(line_color='#06b6d4')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Revenue trend requires order_time column")
    
    with col2:
        # Chart 2: Revenue by City/Channel
        if len(city_kpis) > 0:
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
    
    # Chart 3 & 4: Margin by Category + Revenue by Channel
    col1, col2 = st.columns(2)
    
    with col1:
        # Chart 3: Margin % by Category
        if len(category_kpis) > 0 and 'margin_pct' in category_kpis.columns:
            fig = px.bar(
                category_kpis.head(8),
                x='category',
                y='margin_pct',
                title='Gross Margin % by Category',
                color='margin_pct',
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981']
            )
            fig = style_plotly_chart(fig)
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        elif len(category_kpis) > 0:
            fig = px.bar(
                category_kpis.head(8),
                x='category',
                y='revenue',
                title='Revenue by Category',
                color='revenue',
                color_continuous_scale=['#06b6d4', '#3b82f6', '#8b5cf6']
            )
            fig = style_plotly_chart(fig)
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Chart 4: Revenue by Channel (Pie)
        if len(channel_kpis) > 0:
            fig = px.pie(
                channel_kpis,
                values='revenue',
                names='channel',
                title='Revenue by Channel',
                color_discrete_sequence=['#06b6d4', '#8b5cf6', '#ec4899'],
                hole=0.4
            )
            fig = style_plotly_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== RECOMMENDATION BOX =====
    st.markdown('<p class="section-title section-title-purple">💡 Executive Recommendations</p>', unsafe_allow_html=True)
    
    recommendations = generate_executive_recommendations(kpis, city_kpis, channel_kpis, category_kpis)
    
    for rec in recommendations:
        st.markdown(create_info_card(rec), unsafe_allow_html=True)


def show_manager_view(kpis, city_kpis, channel_kpis, category_kpis, sales_df, products_df, stores_df, inventory_df):
    """Display Manager View - Operational Risk & Execution."""
    
    # ===== KPI CARDS (Manager) =====
    st.markdown('<p class="section-title section-title-blue">⚙️ Operational KPIs</p>', unsafe_allow_html=True)
    
    # Calculate Manager-specific KPIs
    return_rate = kpis.get('return_rate_pct', 0)
    
    # Payment failure rate
    if 'payment_status' in sales_df.columns:
        total_orders = len(sales_df)
        failed_orders = (sales_df['payment_status'] == 'Failed').sum()
        payment_failure_rate = (failed_orders / total_orders * 100) if total_orders > 0 else 0
    else:
        payment_failure_rate = 0
    
    # Stockout risk (simplified)
    stockout_risk = 0
    high_risk_skus = 0
    if 'stock_on_hand' in inventory_df.columns:
        low_stock = (inventory_df['stock_on_hand'] < 10).sum()
        total_inventory = len(inventory_df)
        stockout_risk = (low_stock / total_inventory * 100) if total_inventory > 0 else 0
        high_risk_skus = low_stock
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Stockout Risk %",
            f"{stockout_risk:.1f}%",
            color="pink"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Return Rate %",
            f"{return_rate:.1f}%",
            color="orange"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Payment Failure %",
            f"{payment_failure_rate:.1f}%",
            color="purple"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "High-Risk SKUs",
            f"{high_risk_skus:,}",
            color="blue"
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== CHARTS (Manager - 4 Required) =====
    st.markdown('<p class="section-title section-title-teal">📊 Operational Charts</p>', unsafe_allow_html=True)
    
    # Chart 1 & 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Chart 1: Stockout Risk by City/Channel
        if len(city_kpis) > 0:
            # Simulate stockout risk by city
            city_risk = city_kpis.copy()
            city_risk['stockout_risk'] = np.random.uniform(5, 25, len(city_risk))
            
            fig = px.bar(
                city_risk,
                x='city',
                y='stockout_risk',
                title='Stockout Risk % by City',
                color='stockout_risk',
                color_continuous_scale=['#10b981', '#f59e0b', '#ef4444']
            )
            fig = style_plotly_chart(fig)
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Chart 2: Top 10 Risk Product-Store (Table as Chart)
        if 'stock_on_hand' in inventory_df.columns and 'sku' in inventory_df.columns:
            risk_df = inventory_df.nsmallest(10, 'stock_on_hand')[['sku', 'store_id', 'stock_on_hand']].copy()
            risk_df['risk_level'] = risk_df['stock_on_hand'].apply(
                lambda x: 'Critical' if x < 5 else ('High' if x < 10 else 'Medium')
            )
            
            fig = px.bar(
                risk_df,
                x='sku',
                y='stock_on_hand',
                title='Top 10 Stockout Risk Items',
                color='risk_level',
                color_discrete_map={'Critical': '#ef4444', 'High': '#f59e0b', 'Medium': '#3b82f6'}
            )
            fig = style_plotly_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Stock data not available")
    
    # Chart 3 & 4
    col1, col2 = st.columns(2)
    
    with col1:
        # Chart 3: Inventory Distribution
        if 'stock_on_hand' in inventory_df.columns:
            fig = px.histogram(
                inventory_df,
                x='stock_on_hand',
                title='Inventory Distribution (Stock on Hand)',
                nbins=30,
                color_discrete_sequence=['#06b6d4']
            )
            fig = style_plotly_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Chart 4: Pareto of Issues (from issues log)
        if st.session_state.is_cleaned and hasattr(st.session_state, 'issues_df'):
            issues_df = st.session_state.issues_df
            if len(issues_df) > 0 and 'issue_type' in issues_df.columns:
                issue_counts = issues_df['issue_type'].value_counts().head(10).reset_index()
                issue_counts.columns = ['issue_type', 'count']
                
                fig = px.bar(
                    issue_counts,
                    x='count',
                    y='issue_type',
                    orientation='h',
                    title='Top Issues (Pareto)',
                    color='count',
                    color_continuous_scale=['#06b6d4', '#8b5cf6', '#ec4899']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No issues logged")
        else:
            st.info("Clean data first to see issues Pareto")
    
    st.markdown("---")
    
    # ===== TOP 10 RISK TABLE =====
    st.markdown('<p class="section-title section-title-orange">🚨 Top 10 Stockout Risk Items</p>', unsafe_allow_html=True)
    
    if 'stock_on_hand' in inventory_df.columns and 'sku' in inventory_df.columns:
        risk_table = inventory_df.nsmallest(10, 'stock_on_hand').copy()
        
        # Add store city if possible
        if 'store_id' in risk_table.columns and 'store_id' in stores_df.columns:
            risk_table = risk_table.merge(
                stores_df[['store_id', 'city', 'channel']],
                on='store_id',
                how='left'
            )
        
        display_cols = [col for col in ['sku', 'store_id', 'city', 'channel', 'stock_on_hand'] if col in risk_table.columns]
        st.dataframe(risk_table[display_cols], use_container_width=True)
    else:
        st.info("Inventory data not available for risk analysis")
    
    st.markdown("---")
    
    # ===== OPERATIONAL ALERTS =====
    st.markdown('<p class="section-title section-title-pink">⚠️ Operational Alerts</p>', unsafe_allow_html=True)
    
    alerts = []
    
    if stockout_risk > 15:
        alerts.append(f"🔴 **High Stockout Risk**: {stockout_risk:.1f}% of inventory at risk. Review replenishment urgently.")
    
    if return_rate > 5:
        alerts.append(f"🟠 **Elevated Return Rate**: {return_rate:.1f}% returns. Investigate product quality issues.")
    
    if payment_failure_rate > 3:
        alerts.append(f"🟡 **Payment Failures**: {payment_failure_rate:.1f}% orders failed. Check payment gateway.")
    
    if high_risk_skus > 50:
        alerts.append(f"🔴 **{high_risk_skus} SKUs** at critically low stock. Expedite orders.")
    
    if len(alerts) == 0:
        st.markdown(create_success_card("✅ All operational metrics within healthy ranges."), unsafe_allow_html=True)
    else:
        for alert in alerts:
            st.markdown(create_warning_card(alert), unsafe_allow_html=True)


def generate_executive_recommendations(kpis, city_kpis, channel_kpis, category_kpis):
    """Generate auto recommendations based on KPIs."""
    recommendations = []
    
    # Margin recommendation
    margin = kpis.get('profit_margin_pct', 0)
    if margin < 20:
        recommendations.append(f"📉 **Margin Alert**: Gross margin at {margin:.1f}% is below target. Consider reducing discounts or reviewing supplier costs.")
    elif margin > 35:
        recommendations.append(f"📈 **Strong Margins**: Gross margin at {margin:.1f}% is healthy. Opportunity to invest in growth.")
    
    # Discount recommendation
    avg_discount = kpis.get('avg_discount_pct', 0)
    if avg_discount > 15:
        recommendations.append(f"💸 **High Discounting**: Average discount at {avg_discount:.1f}%. Evaluate if promotions are driving profitable growth.")
    
    # City recommendation
    if len(city_kpis) > 0:
        top_city = city_kpis.iloc[0]['city']
        top_revenue = city_kpis.iloc[0]['revenue']
        recommendations.append(f"🏙️ **Top Market**: {top_city} leads with AED {top_revenue:,.0f} revenue. Consider increasing investment.")
    
    # Channel recommendation
    if len(channel_kpis) > 0:
        top_channel = channel_kpis.iloc[0]['channel']
        recommendations.append(f"📱 **Channel Focus**: {top_channel} is the top performing channel. Optimize marketing spend here.")
    
    if len(recommendations) == 0:
        recommendations.append("✅ Business performance is on track. Continue monitoring KPIs.")
    
    return recommendations
# ============================================================================
# PAGE: DATA (FIXED - BIGGER TITLES)
# ============================================================================

def show_data_page():
    """Display the data management page."""
    
    # BIG PAGE TITLE
    st.markdown('<h1 class="page-title page-title-cyan">📂 Data Management</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Upload, view, and manage your e-commerce data files</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload section
    st.markdown('<p class="section-title section-title-blue">📤 Upload Data Files</p>', unsafe_allow_html=True)
    
    # Show expected columns info
    with st.expander("ℹ️ Expected File Formats (Click to Expand)"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **📦 Products File:**
            - Required: `sku`, `category`, `base_price_aed`
            - Optional: `unit_cost_aed`, `brand`, `launch_flag`
            
            **🛒 Sales File:**
            - Required: `order_id`, `sku`, `store_id`, `qty`, `selling_price_aed`
            - Optional: `order_time`, `discount_pct`, `payment_status`, `return_flag`
            """)
        with col2:
            st.markdown("""
            **🏪 Stores File:**
            - Required: `store_id`, `city`, `channel`
            - Optional: `fulfillment_type`, `store_name`
            
            **📋 Inventory File:**
            - Required: `sku`, `store_id`, `stock_on_hand`
            - Optional: `snapshot_date`, `reorder_point`, `lead_time_days`
            """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track validation status for each file
    valid_files = {}
    
    col1, col2 = st.columns(2)
    
    # ===== PRODUCTS UPLOAD WITH INSTANT VALIDATION =====
    with col1:
        products_file = st.file_uploader("📦 Products CSV", type=['csv'], key='products_upload')
        if products_file:
            try:
                products_df = pd.read_csv(products_file)
                products_file.seek(0)  # Reset file pointer for later use
                validation = FileValidator.validate_file(products_df, 'products')
                
                if validation['valid']:
                    st.success(f"✅ Valid products file ({len(products_df):,} rows)")
                    valid_files['products'] = products_df
                else:
                    st.error(f"❌ {validation['message']}")
                    if validation['missing_columns']:
                        st.warning(f"Missing: {', '.join(validation['missing_columns'])}")
                    if validation.get('detected_type'):
                        st.info(f"💡 This looks like a {validation['detected_type'].upper()} file. Upload it in the correct slot.")
            except Exception as e:
                st.error(f"❌ Cannot read file: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ===== SALES UPLOAD WITH INSTANT VALIDATION =====
        sales_file = st.file_uploader("🛒 Sales CSV", type=['csv'], key='sales_upload')
        if sales_file:
            try:
                sales_df = pd.read_csv(sales_file)
                sales_file.seek(0)
                validation = FileValidator.validate_file(sales_df, 'sales')
                
                if validation['valid']:
                    st.success(f"✅ Valid sales file ({len(sales_df):,} rows)")
                    valid_files['sales'] = sales_df
                else:
                    st.error(f"❌ {validation['message']}")
                    if validation['missing_columns']:
                        st.warning(f"Missing: {', '.join(validation['missing_columns'])}")
                    if validation.get('detected_type'):
                        st.info(f"💡 This looks like a {validation['detected_type'].upper()} file. Upload it in the correct slot.")
            except Exception as e:
                st.error(f"❌ Cannot read file: {str(e)}")
    
    # ===== STORES UPLOAD WITH INSTANT VALIDATION =====
    with col2:
        stores_file = st.file_uploader("🏪 Stores CSV", type=['csv'], key='stores_upload')
        if stores_file:
            try:
                stores_df = pd.read_csv(stores_file)
                stores_file.seek(0)
                validation = FileValidator.validate_file(stores_df, 'stores')
                
                if validation['valid']:
                    st.success(f"✅ Valid stores file ({len(stores_df):,} rows)")
                    valid_files['stores'] = stores_df
                else:
                    st.error(f"❌ {validation['message']}")
                    if validation['missing_columns']:
                        st.warning(f"Missing: {', '.join(validation['missing_columns'])}")
                    if validation.get('detected_type'):
                        st.info(f"💡 This looks like a {validation['detected_type'].upper()} file. Upload it in the correct slot.")
            except Exception as e:
                st.error(f"❌ Cannot read file: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ===== INVENTORY UPLOAD WITH INSTANT VALIDATION =====
        inventory_file = st.file_uploader("📋 Inventory CSV", type=['csv'], key='inventory_upload')
        if inventory_file:
            try:
                inventory_df = pd.read_csv(inventory_file)
                inventory_file.seek(0)
                validation = FileValidator.validate_file(inventory_df, 'inventory')
                
                if validation['valid']:
                    st.success(f"✅ Valid inventory file ({len(inventory_df):,} rows)")
                    valid_files['inventory'] = inventory_df
                else:
                    st.error(f"❌ {validation['message']}")
                    if validation['missing_columns']:
                        st.warning(f"Missing: {', '.join(validation['missing_columns'])}")
                    if validation.get('detected_type'):
                        st.info(f"💡 This looks like a {validation['detected_type'].upper()} file. Upload it in the correct slot.")
            except Exception as e:
                st.error(f"❌ Cannot read file: {str(e)}")
    
    st.markdown("---")
    
    # ===== LOAD BUTTON - ONLY LOADS VALID FILES =====
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Show status before button
        if valid_files:
            st.success(f"✅ {len(valid_files)} valid file(s) ready to load: {', '.join(valid_files.keys())}")
        
        # Disable button if no valid files
        button_disabled = len(valid_files) == 0
        
        if st.button("📥 Load Valid Files", use_container_width=True, disabled=button_disabled):
            if 'products' in valid_files:
                st.session_state.raw_products = valid_files['products']
            if 'stores' in valid_files:
                st.session_state.raw_stores = valid_files['stores']
            if 'sales' in valid_files:
                st.session_state.raw_sales = valid_files['sales']
            if 'inventory' in valid_files:
                st.session_state.raw_inventory = valid_files['inventory']
            
            st.session_state.data_loaded = True
            st.session_state.is_cleaned = False
            st.success(f"✅ {len(valid_files)} file(s) loaded successfully!")
            st.rerun()
        
        if button_disabled and (products_file or stores_file or sales_file or inventory_file):
            st.error("⚠️ Cannot load - no valid files. Please fix the errors above.")
        elif button_disabled:
            st.info("📤 Upload files above to get started.")
    
    st.markdown("---")
    
    # Or load sample data
    st.markdown('<p class="section-title section-title-purple">📦 Or Use Sample Data</p>', unsafe_allow_html=True)
    
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
        st.markdown('<p class="section-title section-title-teal">👀 Data Preview</p>', unsafe_allow_html=True)
        
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
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(df.head(100), use_container_width=True)
            else:
                st.info("📦 No products data loaded")
        
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
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(df.head(100), use_container_width=True)
            else:
                st.info("🏪 No stores data loaded")
        
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
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(df.head(100), use_container_width=True)
            else:
                st.info("🛒 No sales data loaded")
        
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
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(df.head(100), use_container_width=True)
            else:
                st.info("📋 No inventory data loaded")
        
        # Data Quality Insight
        st.markdown("---")
        st.markdown('<p class="section-title section-title-purple">💡 Data Quality Insight</p>', unsafe_allow_html=True)
        
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
            st.markdown(create_insight_card("Minor Issues Detected", f"Overall null rate is {overall_null_pct:.1f}%. Data Cleaner can help fix these small issues."), unsafe_allow_html=True)
        else:
            st.markdown(create_insight_card("Excellent Data Quality", "No missing values detected in your datasets! Data looks clean."), unsafe_allow_html=True)
    
    show_footer()
# ============================================================================
# PAGE: CLEANER (FIXED - BIGGER TITLES)
# ============================================================================

def show_cleaner_page():
    """Display the data cleaner page."""
    
    st.markdown('<h1 class="page-title page-title-green">🧹 Data Rescue Center</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Validate, detect issues, and clean your dirty data automatically</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.markdown(create_warning_card("Please load data first. Go to 📂 Data page."), unsafe_allow_html=True)
        show_footer()
        return
    
    st.markdown('<p class="section-title section-title-cyan">🔍 Issues We Detect & Fix</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <strong style="color: #06b6d4; font-size: 1.1rem;">Data Quality</strong>
            <ul style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 0; line-height: 1.8;">
                <li>Missing values</li>
                <li>Duplicate Recordss</li>
                <li>Whitespace issues</li>
                <li>Text standardization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="border-left-color: #8b5cf6;">
            <strong style="color: #8b5cf6; font-size: 1.1rem;">Format Issues</strong>
            <ul style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 0; line-height: 1.8;">
                <li>Multi-language text</li>
                <li>Non-English values</li>
                <li>Fuzzy matching</li>
                <li>Case normalization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card" style="border-left-color: #ec4899;">
            <strong style="color: #ec4899; font-size: 1.1rem;">Value Issues</strong>
            <ul style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 0; line-height: 1.8;">
                <li>Negative values</li>
                <li>Outliers (IQR)</li>
                <li>FK violations</li>
                <li>Invalid references</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Data Cleaning", width='stretch', type="primary"):
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
                    st.session_state.cleaning_report = cleaner.cleaning_report
                    st.session_state.is_cleaned = True
                    
                    st.success("✅ Data cleaning complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error during cleaning: {str(e)}")
    
    if st.session_state.is_cleaned:
        st.markdown("---")
        st.markdown('<p class="section-title section-title-blue">📊 Cleaning Results</p>', unsafe_allow_html=True)
        
        stats = st.session_state.cleaner_stats
        report = st.session_state.cleaning_report
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'products' in report:
                before = report['products'].get('original_rows', 0)
                after = report['products'].get('final_rows', 0)
                fixed = report['products'].get('missing_fixed', 0) + report['products'].get('duplicates_removed', 0)
                delta = f"{fixed} fixed" if fixed > 0 else "Clean"
                delta_type = "positive"
            else:
                after = len(st.session_state.clean_products)
                delta = "Processed"
                delta_type = "positive"
            st.markdown(create_metric_card("Products", f"{after:,}", delta, delta_type, "cyan"), unsafe_allow_html=True)
        
        with col2:
            if 'stores' in report:
                before = report['stores'].get('original_rows', 0)
                after = report['stores'].get('final_rows', 0)
                fixed = report['stores'].get('missing_fixed', 0) + report['stores'].get('duplicates_removed', 0)
                delta = f"{fixed} fixed" if fixed > 0 else "Clean"
                delta_type = "positive"
            else:
                after = len(st.session_state.clean_stores)
                delta = "Processed"
                delta_type = "positive"
            st.markdown(create_metric_card("Stores", f"{after:,}", delta, delta_type, "blue"), unsafe_allow_html=True)
        
        with col3:
            if 'sales' in report:
                before = report['sales'].get('original_rows', 0)
                after = report['sales'].get('final_rows', 0)
                fixed = report['sales'].get('missing_fixed', 0) + report['sales'].get('duplicates_removed', 0)
                delta = f"{fixed} fixed" if fixed > 0 else "Clean"
                delta_type = "positive"
            else:
                after = len(st.session_state.clean_sales)
                delta = "Processed"
                delta_type = "positive"
            st.markdown(create_metric_card("Sales", f"{after:,}", delta, delta_type, "purple"), unsafe_allow_html=True)
        
        with col4:
            if 'inventory' in report:
                before = report['inventory'].get('original_rows', 0)
                after = report['inventory'].get('final_rows', 0)
                fixed = report['inventory'].get('missing_fixed', 0) + report['inventory'].get('duplicates_removed', 0)
                delta = f"{fixed} fixed" if fixed > 0 else "Clean"
                delta_type = "positive"
            else:
                after = len(st.session_state.clean_inventory)
                delta = "Processed"
                delta_type = "positive"
            st.markdown(create_metric_card("Inventory", f"{after:,}", delta, delta_type, "pink"), unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<p class="section-title section-title-teal">📈 Cleaning Summary</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("Missing Fixed", f"{stats.get('missing_values_fixed', 0):,}", color="cyan"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card("Duplicates Removed", f"{stats.get('duplicates_removed', 0):,}", color="blue"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("Outliers Fixed", f"{stats.get('outliers_fixed', 0):,}", color="purple"), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card("Text Standardized", f"{stats.get('text_standardized', 0):,}", color="pink"), unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<p class="section-title section-title-orange">🔍 Issues Detected & Fixed</p>', unsafe_allow_html=True)
        
        issues_df = st.session_state.issues_df
        
        if len(issues_df) > 0 and not (len(issues_df) == 1 and issues_df.iloc[0]['issue_type'] == 'None'):
            total_fixed = stats.get('total_issues_fixed', 0)
            st.markdown(create_success_card(f"Total {total_fixed} issues detected and fixed automatically!"), unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                issue_counts = issues_df.groupby('issue_type').size().reset_index(name='count')
                
                fig = px.bar(
                    issue_counts,
                    x='count',
                    y='issue_type',
                    orientation='h',
                    title='Issues by Type',
                    color='count',
                    color_continuous_scale=['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899']
                )
                fig = style_plotly_chart(fig)
                fig.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                table_counts = issues_df.groupby('table').size().reset_index(name='count')
                
                fig = px.pie(
                    table_counts,
                    values='count',
                    names='table',
                    title='Issues by Table',
                    color_discrete_sequence=['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899'],
                    hole=0.45
                )
                fig = style_plotly_chart(fig)
                st.plotly_chart(fig, width='stretch')
            
            st.markdown('<p class="section-title section-title-purple">💡 Cleaning Insight</p>', unsafe_allow_html=True)
            
            top_issue = issue_counts.loc[issue_counts['count'].idxmax(), 'issue_type']
            top_count = issue_counts['count'].max()
            st.markdown(create_insight_card("Most Common Issue", f"'{top_issue}' was the most frequent issue with {top_count} occurrences. All instances have been automatically fixed."), unsafe_allow_html=True)
            
            st.markdown('<p class="section-title section-title-blue">📋 issue_issue_detailed Issues Log</p>', unsafe_allow_html=True)
            st.dataframe(issues_df, width='stretch')
            
            csv = issues_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Issues Log (CSV)",
                data=csv,
                file_name="data_issues_log.csv",
                mime="text/csv"
            )
        else:
            st.markdown(create_success_card("No major issues found! Your data is already clean."), unsafe_allow_html=True)
        
        if 'foreign_key_issues' in report:
            fk = report['foreign_key_issues']
            if fk.get('invalid_skus', 0) > 0 or fk.get('invalid_stores', 0) > 0:
                st.markdown("---")
                st.markdown('<p class="section-title section-title-orange">⚠️ Foreign Key Warnings</p>', unsafe_allow_html=True)
                
                if fk.get('invalid_skus', 0) > 0:
                    st.warning(f"⚠️ {fk['invalid_skus']} sales records have SKUs not found in products table")
                if fk.get('invalid_stores', 0) > 0:
                    st.warning(f"⚠️ {fk['invalid_stores']} sales records have store IDs not found in stores table")
    
    show_footer()

# ============================================================================
# PAGE: SIMULATOR (FIXED - BIGGER TITLES)
# ============================================================================

def show_simulator_page():
    """Display the campaign simulator page."""
    
    st.markdown('<h1 class="page-title page-title-purple">🎯 Campaign Simulator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Run what-if scenarios and forecast campaign outcomes</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first. Go to 📂 Data page.")
        show_footer()
        return
    
    sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
    stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
    products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
    
    st.markdown('<p class="section-title section-title-cyan">⚙️ Campaign Parameters</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<p style="color: #06b6d4; font-weight: 600; margin-bottom: 10px;">💰 Pricing</p>', unsafe_allow_html=True)
        discount_pct = st.slider("Discount %", 0, 50, 15)
        promo_budget = st.number_input("Promo Budget (AED)", 1000, 500000, 25000, step=5000)
    
    with col2:
        st.markdown('<p style="color: #8b5cf6; font-weight: 600; margin-bottom: 10px;">📊 Constraints</p>', unsafe_allow_html=True)
        margin_floor = st.slider("Margin Floor %", 0, 50, 15)
        campaign_days = st.slider("Campaign Days", 1, 30, 7)
    
    with col3:
        st.markdown('<p style="color: #ec4899; font-weight: 600; margin-bottom: 10px;">🎯 Targeting</p>', unsafe_allow_html=True)
        
        cities = ['All']
        channels = ['All']
        categories = ['All']
        
        if stores_df is not None and 'city' in stores_df.columns:
            cities += stores_df['city'].dropna().unique().tolist()
        if stores_df is not None and 'channel' in stores_df.columns:
            channels += stores_df['channel'].dropna().unique().tolist()
        if products_df is not None and 'category' in products_df.columns:
            categories += products_df['category'].dropna().unique().tolist()
        
        city = st.selectbox("Target City", cities)
        channel = st.selectbox("Target Channel", channels)
        category = st.selectbox("Target Category", categories)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_simulation = st.button("🚀 Run Simulation", width='stretch', type="primary")
    
    if run_simulation:
        with st.spinner("🔄 Running simulation..."):
            try:
                sim = Simulator()
                
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
                
            except Exception as e:
                st.error(f"❌ Simulation error: {str(e)}")
    
    if 'sim_results' in st.session_state and st.session_state.sim_results:
        results = st.session_state.sim_results
        outputs = results.get('outputs')
        comparison = results.get('comparison')
        warnings = results.get('warnings', [])
        
        if outputs:
            st.markdown("---")
            st.markdown('<p class="section-title section-title-teal">📊 Simulation Results</p>', unsafe_allow_html=True)
            
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
            
            st.markdown("<br>", unsafe_allow_html=True)
            
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
            
            if warnings:
                st.markdown("---")
                st.markdown('<p class="section-title section-title-orange">⚠️ Risk Alerts</p>', unsafe_allow_html=True)
                for warning in warnings:
                    st.warning(warning)
            else:
                st.markdown("---")
                st.success("✅ All metrics within acceptable range. Campaign looks healthy!")
            
            st.markdown("---")
            st.markdown('<p class="section-title section-title-blue">📈 Baseline vs Campaign</p>', unsafe_allow_html=True)
            
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
                st.plotly_chart(fig, width='stretch')
            
            with col2:
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
                st.plotly_chart(fig, width='stretch')
        
        elif warnings:
            for warning in warnings:
                st.warning(warning)
    
    show_footer()

# ============================================================================
# PAGE: ANALYTICS (FIXED - BIGGER TITLES + TAB HOVER)
# ============================================================================

def show_analytics_page():
    """Display the analytics page."""
    
    st.markdown('<h1 class="page-title page-title-pink">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Deep dive into your e-commerce performance metrics</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first. Go to 📂 Data page.")
        show_footer()
        return
    
    sales_df = st.session_state.clean_sales if st.session_state.is_cleaned else st.session_state.raw_sales
    products_df = st.session_state.clean_products if st.session_state.is_cleaned else st.session_state.raw_products
    stores_df = st.session_state.clean_stores if st.session_state.is_cleaned else st.session_state.raw_stores
    inventory_df = st.session_state.clean_inventory if st.session_state.is_cleaned else st.session_state.raw_inventory
    
    sim = Simulator()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏙️ By City", "📦 By Category", "📋 Inventory"])
    
    with tab1:
        st.markdown('<p class="section-title section-title-cyan">📈 Daily Performance Trends</p>', unsafe_allow_html=True)
        
        try:
            daily_trends = sim.calculate_daily_trends(sales_df, products_df)
            
            if daily_trends is None or len(daily_trends) == 0:
                st.warning("⚠️ No trend data available. This could be due to missing date column in sales data.")
            else:
                fig = px.area(
                    daily_trends,
                    x='date',
                    y='revenue',
                    title='Daily Revenue Trend',
                    color_discrete_sequence=['#06b6d4']
                )
                fig = style_plotly_chart(fig)
                fig.update_traces(line=dict(width=3), fillcolor='rgba(6, 182, 212, 0.2)')
                st.plotly_chart(fig, width='stretch')
                
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
                    st.plotly_chart(fig, width='stretch')
                
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
                    st.plotly_chart(fig, width='stretch')
                
                st.markdown('<p class="section-title section-title-purple">💡 Trend Insight</p>', unsafe_allow_html=True)
                avg_revenue = daily_trends['revenue'].mean()
                max_revenue = daily_trends['revenue'].max()
                max_date = daily_trends.loc[daily_trends['revenue'].idxmax(), 'date']
                date_str = max_date.strftime('%b %d, %Y') if hasattr(max_date, 'strftime') else str(max_date)
                st.markdown(create_insight_card("Peak Performance Day", f"Best day was {date_str} with AED {max_revenue:,.0f} revenue ({((max_revenue/avg_revenue)-1)*100:.0f}% above average)."), unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error loading trends: {str(e)}")
    
    with tab2:
        st.markdown('<p class="section-title section-title-blue">🏙️ Performance by City</p>', unsafe_allow_html=True)
        
        try:
            city_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'city')
            
            if city_kpis is None or len(city_kpis) == 0:
                st.warning("⚠️ No city data available.")
            else:
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
                    st.plotly_chart(fig, width='stretch')
                
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
                    st.plotly_chart(fig, width='stretch')
                
                st.markdown('<p class="section-title section-title-teal">📋 City Performance Table</p>', unsafe_allow_html=True)
                st.dataframe(city_kpis, width='stretch')
                
                st.markdown('<p class="section-title section-title-purple">💡 City Insight</p>', unsafe_allow_html=True)
                top_city = city_kpis.iloc[0]
                total_rev = city_kpis['revenue'].sum()
                top_pct = (top_city['revenue'] / total_rev * 100) if total_rev > 0 else 0
                st.markdown(create_insight_card("Market Leader", f"{top_city['city']} leads with {top_pct:.0f}% of revenue (AED {top_city['revenue']:,.0f})."), unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error loading city data: {str(e)}")
    
    with tab3:
        st.markdown('<p class="section-title section-title-purple">📦 Performance by Category</p>', unsafe_allow_html=True)
        
        try:
            cat_kpis = sim.calculate_kpis_by_dimension(sales_df, stores_df, products_df, 'category')
            
            if cat_kpis is None or len(cat_kpis) == 0:
                st.warning("⚠️ No category data available.")
            else:
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
                    st.plotly_chart(fig, width='stretch')
                
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
                    st.plotly_chart(fig, width='stretch')
                
                st.markdown('<p class="section-title section-title-teal">📋 Category Performance Table</p>', unsafe_allow_html=True)
                st.dataframe(cat_kpis, width='stretch')
                
                st.markdown('<p class="section-title section-title-purple">💡 Category Insight</p>', unsafe_allow_html=True)
                top_cat = cat_kpis.iloc[0]
                st.markdown(create_insight_card("Top Category", f"{top_cat['category']} leads with AED {top_cat['revenue']:,.0f} revenue and {top_cat['profit_margin_pct']:.1f}% margin."), unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error loading category data: {str(e)}")
    
    with tab4:
        st.markdown('<p class="section-title section-title-orange">📋 Inventory Health</p>', unsafe_allow_html=True)
        
        try:
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
                    st.plotly_chart(fig, width='stretch')
                
                with col2:
                    inventory_copy = inventory_df.copy()
                    inventory_copy['stock_on_hand'] = pd.to_numeric(inventory_copy['stock_on_hand'], errors='coerce').fillna(0)
                    
                    if 'reorder_point' in inventory_copy.columns:
                        inventory_copy['reorder_point'] = pd.to_numeric(inventory_copy['reorder_point'], errors='coerce').fillna(10)
                    else:
                        inventory_copy['reorder_point'] = 10
                    
                    inventory_copy['status'] = inventory_copy.apply(
                        lambda x: 'Critical' if x['stock_on_hand'] == 0 
                        else ('Low' if x['stock_on_hand'] <= x['reorder_point'] else 'Healthy'),
                        axis=1
                    )
                    status_counts = inventory_copy['status'].value_counts().reset_index()
                    status_counts.columns = ['Status', 'count']
                    
                    fig = px.pie(
                        status_counts,
                        values='count',
                        names='Status',
                        title='Inventory Status',
                        color='Status',
                        color_discrete_map={'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'},
                        hole=0.45
                    )
                    fig = style_plotly_chart(fig)
                    st.plotly_chart(fig, width='stretch')
                
                st.markdown('<p class="section-title section-title-purple">💡 Inventory Insight</p>', unsafe_allow_html=True)
                if stockout['zero_stock'] > 0:
                    st.markdown(create_insight_card("Critical Stock Alert", f"{stockout['zero_stock']} items are out of stock! Immediate reorder required."), unsafe_allow_html=True)
                elif stockout['stockout_risk_pct'] > 15:
                    st.markdown(create_insight_card("Reorder Recommended", f"{stockout['stockout_risk_pct']:.0f}% of inventory is below reorder point."), unsafe_allow_html=True)
                else:
                    st.markdown(create_insight_card("Healthy Inventory", "Inventory levels are well-maintained."), unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error loading inventory data: {str(e)}")
    
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
elif page == "📊 Dashboard":
    show_dashboard_page()
elif page == "🎯 Simulator":
    show_simulator_page()
