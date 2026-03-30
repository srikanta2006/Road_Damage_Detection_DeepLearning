import streamlit as st
import pandas as pd
import time
import os
from utils.alerts import render_sidebar_alerts

st.set_page_config(
    page_title="SRIMS | AI Road Infrastructure Management",
    page_icon="🚧",
    layout="wide"
)

render_sidebar_alerts()

# Custom Glassmorphism CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [data-testid="stSidebar"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background: radial-gradient(circle at top right, #1a1c2c, #0E1117);
}

.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 25px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(255, 75, 75, 0.4);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.stat-value {
    font-size: 32px;
    font-weight: 800;
    color: #FF4B4B;
}

.stat-label {
    font-size: 14px;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

h1 {
    font-weight: 800;
    background: linear-gradient(90deg, #FF4B4B, #FF8F8F);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 40px !important;
}

.stButton>button {
    background: linear-gradient(90deg, #FF4B4B, #FF2B2B);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 12px 25px;
    transition: all 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚧 Smart Road Infrastructure Management System (SRIMS)</h1>", unsafe_allow_html=True)

# --- DYNAMIC DATA SYNC: REAL-TIME CSV TRACKING ---
if os.path.exists("gps_log.csv"):
    df = pd.read_csv("gps_log.csv")
    active_det = len(df[df['status'] != 'Resolved'])
    total_inspected = len(df)
    system_status = "Online"
else:
    active_det = 0
    total_inspected = 0
    system_status = "Awaiting Logic"

# Hero Section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='glass-card'>
        <div class='stat-label'>Total Infrastructure Audit</div>
        <div class='stat-value'>{total_inspected} Points</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='glass-card'>
        <div class='stat-label'>Unresolved Hazards</div>
        <div class='stat-value'>{active_det} Active</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    color = "#4CAF50" if active_det == 0 and total_inspected > 0 else "#FFC107" if active_det > 0 else "#888"
    st.markdown(f"""
    <div class='glass-card'>
        <div class='stat-label'>Operational Grid Status</div>
        <div class='stat-value' style='color: {color};'>{system_status}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Feature Showcase
col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.markdown("## 🔍 Intelligence Engine")
    st.write("""
    SRIMS uses deep learning (YOLOv8) to automate road surveys, identifying 
    4 critical damage types with high confidence.
    """)
    
    st.markdown("""
    - **Live Stream Analysis** (Webcam/Drone Support)
    - **Batch Processing** (Upload images or high-res videos)
    - **Strategic Analytics** (Predictive RHI & Cost Mapping)
    """)
    
    if st.button("🚀 Begin New Survey"):
        st.info("Select a detection module from the sidebar to start a new mission.")

with col_right:
    st.markdown("### 📊 Live Operational Health")
    health_score = 100 - (active_det * 2) if total_inspected > 0 else 100
    health_score = max(50, min(100, health_score))
    st.progress(health_score / 100, text=f"City Infrastructure Integrity: {health_score}%")
    st.caption("Real-time synchronization with active field maintenance status.")

st.markdown("---")

# Footer
st.markdown("<p style='text-align:center; color: #555;'>Ministry of Public Works | Smart Infrastructure Initiative</p>", unsafe_allow_html=True)
