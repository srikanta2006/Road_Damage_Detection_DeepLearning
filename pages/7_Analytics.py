import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from utils.alerts import render_sidebar_alerts

st.set_page_config(page_title="Infrastructure Intelligence Pro", page_icon="🏢", layout="wide")

render_sidebar_alerts()

# PREMIUM MANAGEMENT THEME
st.markdown("""
<style>
.main { background: radial-gradient(circle at top left, #0D1117, #161B22); }
.metric-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-5px); border-color: #3498DB; }
.grade-badge { font-size: 38px; font-weight: 900; margin: 5px 0; }
.grade-A { color: #2ECC71; }
.grade-B { color: #3498DB; }
.grade-C { color: #F1C40F; }
.grade-D { color: #E67E22; }
.grade-F { color: #E74C3C; }
.stat-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
.stat-value { font-size: 18px; font-weight: bold; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🏛️ 360° Infrastructure Intelligence Pro")

# Load Data
if os.path.exists("gps_log.csv"):
    df = pd.read_csv("gps_log.csv")
else:
    st.warning("Spatial database unavailable. Run a sensor detection to begin.")
    st.stop()

if df.empty:
    st.warning("Infrastructure log exists but is currently empty.")
    st.stop()

# --- DYNAMIC DATA SYNC: ONLY COUNT ACTIVE HAZARDS ---
total_detections = len(df)
active_df = df[df['status'] != 'Resolved'].copy()
resolved_df = df[df['status'] == 'Resolved'].copy()

# Critical Metrics (Recalculated)
high_sev = len(active_df[active_df['severity'] == 'high'])
medium_sev = len(active_df[active_df['severity'] == 'medium'])
low_sev = len(active_df[active_df['severity'] == 'low'])
resolved_count = len(resolved_df)
pending_count = len(active_df)

# Road Health Index (RHI) - Corrected logic: Fewer pending = Higher score
# Max RHI is 100. Each pending high severity deducts 15 points, etc.
penalty = (high_sev * 15) + (medium_sev * 5) + (low_sev * 1)
rhi_score = 100 - (penalty / (total_detections if total_detections > 0 else 1) * 3)
rhi_score = max(0, min(100, rhi_score))

# Maintenance Velocity
vel_score = (resolved_count / total_detections) * 100 if total_detections > 0 else 0

# Citizen Satisfaction (CSAT) 
csat_score = (rhi_score * 0.6) + (vel_score * 0.4)
csat_color = "#2ECC71" if csat_score > 75 else "#F1C40F" if csat_score > 50 else "#E74C3C"

# System Quality Index (SQI) 
sqi_score = df['confidence'].mean() * 100 if total_detections > 0 else 0

# Infrastructure Grade
grade = "A+" if rhi_score > 95 else "A" if rhi_score > 85 else "B" if rhi_score > 70 else "C" if rhi_score > 55 else "D" if rhi_score > 40 else "F"
grade_class = f"grade-{grade[0]}"

# --- ROW 1: PRIMARY STRATEGIC DIALS ---
st.markdown("#### 🔘 Real-Time Strategic Performance Indicators")
d1, d2, d3, d4 = st.columns(4)

with d1:
    st.markdown(f"<div class='metric-card'><p class='stat-label'>STRATEGIC HEALTH GRADE</p><div class='grade-badge {grade_class}'>{grade}</div><p class='stat-label'>Active Assessment</p></div>", unsafe_allow_html=True)

with d2:
    fig_rhi = go.Figure(go.Indicator(
        mode = "gauge+number", value = rhi_score,
        title = {'text': "Current Health (RHI)", 'font': {'size': 13}},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#FF4B4B"}, 'bgcolor': "rgba(255,255,255,0.05)"}
    ))
    fig_rhi.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=200, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_rhi, use_container_width=True)

with d3:
    fig_csat = go.Figure(go.Indicator(
        mode = "gauge+number", value = csat_score,
        title = {'text': "Citizen Perception (CSAT)", 'font': {'size': 13}},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': csat_color}, 'bgcolor': "rgba(255,255,255,0.05)"}
    ))
    fig_csat.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=200, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_csat, use_container_width=True)

with d4:
    fig_sqi = go.Figure(go.Indicator(
        mode = "gauge+number", value = sqi_score,
        title = {'text': "Sensor Reliability (SQI)", 'font': {'size': 13}},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#3498DB"}, 'bgcolor': "rgba(255,255,255,0.05)"}
    ))
    fig_sqi.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=200, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_sqi, use_container_width=True)

st.divider()

# --- ROW 2: OPERATIONAL FORECASTING ---
mat_potholes = len(active_df[active_df['damage_type'] == 'Potholes']) * 0.8
mat_cracks = len(active_df[active_df['damage_type'] != 'Potholes']) * 0.3
total_material = mat_potholes + mat_cracks

st.markdown("#### 🏗️ Synchronized Operational Intelligence")
o1, o2, o3, o4 = st.columns(4)

with o1:
    st.markdown(f"""<div class='metric-card'><p class='stat-label'>Material Forecast</p><div class='stat-value'>{total_material:.1f} Tons</div><p class='stat-label'>Pending Construction</p></div>""", unsafe_allow_html=True)
with o2:
    p_liability = pending_count * 3200
    st.markdown(f"""<div class='metric-card'><p class='stat-label'>Active Liability</p><div class='stat-value'>₹{p_liability:,}</div><p class='stat-label'>Fiscal Risk Exposure</p></div>""", unsafe_allow_html=True)
with o3:
    st.markdown(f"""<div class='metric-card'><p class='stat-label'>Pending Repairs</p><div class='stat-value'>{pending_count} Items</div><p class='stat-label'>Live Operational Queue</p></div>""", unsafe_allow_html=True)
with o4:
    st.markdown(f"""<div class='metric-card'><p class='stat-label'>Resolved Total</p><div class='stat-value'>{resolved_count} Assets</div><p class='stat-label'>Historical Recovery Rate</p></div>""", unsafe_allow_html=True)

st.divider()

# --- ROW 3: SPATIAL LANDSCAPE ---
c_map1, c_map2 = st.columns([2, 1])

with c_map1:
    st.subheader("🌋 3D Structural Stress Topography")
    # Z-magnitude based only on active hazards for visual accuracy
    df['magnitude'] = df['confidence'] * df['severity'].map({'high': 6, 'medium': 3, 'low': 1})
    # Diminish Resolved markers for focus on pending
    df.loc[df['status'] == 'Resolved', 'magnitude'] = 0.1
    
    fig_3d = px.scatter_3d(df, x='lat', y='lon', z='magnitude', color='severity', size='confidence',
                           color_discrete_map={'high': '#E74C3C', 'medium': '#F39C12', 'low': '#2ECC71'},
                           opacity=0.7)
    fig_3d.update_layout(scene=dict(bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=500, margin=dict(l=0,r=0,b=0,t=0))
    st.plotly_chart(fig_3d, use_container_width=True)

with c_map2:
    st.subheader("🚩 Active Critical Hotspots")
    hotspots = active_df[active_df['severity'] == 'high'].groupby('location_label').size().reset_index(name='Active Alerts').sort_values(by='Active Alerts', ascending=False)
    st.dataframe(hotspots, use_container_width=True, hide_index=True)
    st.caption("AI-identified sectors requiring field intervention.")
    
    if st.button("♻️ Force Dashboard Sync"):
        st.rerun()

st.divider()

# --- ROW 4: DEGRADATION SIMULATOR ---
st.subheader("📉 Road Safety Forecasting (12 Month Projection)")
months = [f"M{i}" for i in range(13)]
vals = []
cur = rhi_score
# Degradation slows as items are resolved
d_rate = 1.0 + (high_sev * 0.4) 
for _ in months:
    vals.append(max(0, cur))
    cur -= (d_rate + np.random.uniform(0.1, 0.3))

fig_sim = go.Figure(go.Scatter(x=months, y=vals, mode='lines', line=dict(color='#3498DB', width=4), fill='tozeroy', fillcolor='rgba(52, 152, 219, 0.1)'))
fig_sim.update_layout(xaxis_title="Timeline", yaxis_title="Structural Integrity", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
st.plotly_chart(fig_sim, use_container_width=True)
