import streamlit as st
import pandas as pd
import time
import os
from utils.alerts import render_sidebar_alerts
from utils.style import apply_custom_style, render_modern_card, render_top_nav

st.set_page_config(
    page_title="SRIMS | Enterprise Infrastructure AI",
    page_icon="🚧",
    layout="wide"
)

# Apply global styling
apply_custom_style()

# Top Navbar
render_top_nav("Home")

# Sidebar
render_sidebar_alerts()

# Hero Section
st.markdown("""
<div class="hero-section animate-in">
    <h1>Smart Road Infrastructure Management System (SRIMS)</h1>
    <p class="hero-tagline">
        Precision AI-driven sensing and analytics suite for automated urban infrastructure auditing and health monitoring.
    </p>
</div>
""", unsafe_allow_html=True)

# --- DYNAMIC DATA SYNC ---
if os.path.exists("gps_log.csv"):
    df = pd.read_csv("gps_log.csv")
    active_det = len(df[df['status'] != 'Resolved'])
    total_inspected = len(df)
    system_status = "Operational"
else:
    active_det = 0
    total_inspected = 0
    system_status = "Booting..."

# Hero Section - Interactive Stats
col1, col2, col3 = st.columns(3)
with col1:
    render_modern_card("Data Points", f"{total_inspected}", "fa-database")
with col2:
    render_modern_card("Active Hazards", f"{active_det}", "fa-triangle-exclamation")
with col3:
    status_icon = "fa-circle-check" if active_det == 0 else "fa-bolt-lightning"
    render_modern_card("System Health", system_status, status_icon)

st.markdown("<br>", unsafe_allow_html=True)

# 🏢 THE SRIMS MISSION
st.markdown("### <i class='fa-solid fa-flag-checkered' style='color: var(--primary-blue);'></i> The SRIMS Mission", unsafe_allow_html=True)
st.markdown("""
<div class="modern-card animate-in" style="background: #FFFFFF; border-left: 5px solid var(--primary-blue);">
    <p style="color: var(--text-slate-900); font-size: 1.1rem; line-height: 1.6; margin: 0;">
        <b>SRIMS</b> (Smart Road Infrastructure Management System) is an industry-grade platform designed to 
        transmute raw sensor data into actionable infrastructure intelligence. By automating municipal audits, 
        we reduce manual survey costs by 85% and ensure 24/7 visibility into urban safety corridors.
    </p>
</div>
""", unsafe_allow_html=True)

# 🧠 CORE TECHNOLOGY STACK
st.markdown("### <i class='fa-solid fa-microchip' style='color: var(--primary-blue);'></i> Under The Hood", unsafe_allow_html=True)
c_tech1, c_tech2, c_tech3 = st.columns(3)

with c_tech1:
    st.markdown("""
    <div class="modern-card" style="height: 220px;">
        <h4 style="margin-top:0;"><i class="fa-solid fa-brain" style="color: var(--primary-blue);"></i> YOLOv8 Edge AI</h4>
        <p style="color: var(--text-slate-600); font-size: 0.9rem;">
            Real-time visual perception engine optimized for structural defect classification (Potholes, Cracks, Alligatoring) 
            with sub-100ms inference latency.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c_tech2:
    st.markdown("""
    <div class="modern-card" style="height: 220px;">
        <h4 style="margin-top:0;"><i class="fa-solid fa-satellite" style="color: var(--primary-blue);"></i> Spatial Core</h4>
        <p style="color: var(--text-slate-600); font-size: 0.9rem;">
            High-precision GNSS telemetry synchronization ensures every detected hazard is spatially grounded 
            for tactical field operation deployment.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c_tech3:
    st.markdown("""
    <div class="modern-card" style="height: 220px;">
        <h4 style="margin-top:0;"><i class="fa-solid fa-chart-line" style="color: var(--primary-blue);"></i> ROI Optimizer</h4>
        <p style="color: var(--text-slate-600); font-size: 0.9rem;">
            Proprietary <i>Road Health Index (RHI)</i> modeling converts physical damage into fiscal 
            liability reports and procurement workplans.
        </p>
    </div>
    """, unsafe_allow_html=True)

# 🛠️ OPERATIONAL PROTOCOLS (1-2-3 Guide)
st.markdown("### <i class='fa-solid fa-stairs' style='color: var(--primary-blue);'></i> Operational Protocol", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

p1.markdown("""
<div style="text-align: center; padding: 20px;">
    <div style="font-size: 2.5rem; color: #E2E8F0; font-weight: 800; margin-bottom: -20px;">01</div>
    <h4 style="color: var(--primary-blue);">DEPLOY</h4>
    <p style="color: var(--text-slate-600); font-size: 0.85rem;">Execute Image, Video, or Live Sensing missions to ingest raw infrastructure data.</p>
</div>
""", unsafe_allow_html=True)

p2.markdown("""
<div style="text-align: center; padding: 20px;">
    <div style="font-size: 2.5rem; color: #E2E8F0; font-weight: 800; margin-bottom: -20px;">02</div>
    <h4 style="color: var(--primary-blue);">OPTIMIZE</h4>
    <p style="color: var(--text-slate-600); font-size: 0.85rem;">Review Tactical Worklists and verify field rectifications via the Ops Center.</p>
</div>
""", unsafe_allow_html=True)

p3.markdown("""
<div style="text-align: center; padding: 20px;">
    <div style="font-size: 2.5rem; color: #E2E8F0; font-weight: 800; margin-bottom: -20px;">03</div>
    <h4 style="color: var(--primary-blue);">STRATEGIC</h4>
    <p style="color: var(--text-slate-600); font-size: 0.85rem;">Generate Strategic Audits and ROI Briefings for procurement and municipal planning.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Feature Showcase Buttons
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.markdown("### <i class='fa-solid fa-play' style='color: var(--primary-blue);'></i> Deployment Portal", unsafe_allow_html=True)
    st.write("""
    Ready to transform your infrastructure survey? Select a sensing payload from the <b>Deployment Core</b> 
    above to begin real-time data ingestion.
    """)
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    if st.button("🚀 INITIATE SURVEY MISSION"):
        st.info("Deploy a diagnostic module from the navigation hub above.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown("### <i class='fa-solid fa-shield-heart' style='color: var(--primary-blue);'></i> Sector Integrity", unsafe_allow_html=True)
    health_score = 100 - (active_det * 3) if total_inspected > 0 else 100
    health_score = max(40, min(100, health_score))
    
    st.progress(health_score / 100)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; color: var(--text-slate-600); font-size: 0.9rem; margin-top: 8px;">
        <span>Operational Health Score Index</span>
        <span style="color: var(--primary-blue); font-weight: 700;">{health_score}%</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

# Footer
st.markdown("""
<div style="text-align: center; color: #94A3B8; padding: 20px; font-size: 0.85rem; letter-spacing: 1.5px;">
    <i class="fa-solid fa-building-shield"></i> MINISTRY OF PUBLIC WORKS | STRATEGIC INFRASTRUCTURE ALLIANCE
</div>
""", unsafe_allow_html=True)
