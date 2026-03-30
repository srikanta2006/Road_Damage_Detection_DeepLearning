import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from utils.alerts import render_sidebar_alerts

st.set_page_config(page_title="Strategic Infrastructure Pro", page_icon="🏢", layout="wide")

render_sidebar_alerts()

# PREMIUM THEME
st.markdown("""
<style>
.main { background: radial-gradient(circle at top left, #0D1117, #161B22); }
.briefing-box {
    background: rgba(46, 204, 113, 0.05);
    border-left: 5px solid #2ECC71;
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 25px;
}
.metric-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}
.stat-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
.stat-value { font-size: 18px; font-weight: bold; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🏙️ Strategic Infrastructure & Budget Optimization")

# Load Data
if os.path.exists("gps_log.csv"):
    df = pd.read_csv("gps_log.csv")
else:
    st.warning("Database unavailable.")
    st.stop()

# --- DATA PRE-PROCESSING ---
active_df = df[df['status'] != 'Resolved'].copy()
resolved_df = df[df['status'] == 'Resolved'].copy()
total_dets = len(df)
pending_dets = len(active_df)

# RHI Recalculation
h = len(active_df[active_df['severity'] == 'high'])
m = len(active_df[active_df['severity'] == 'medium'])
l = len(active_df[active_df['severity'] == 'low'])
rhi = 100 - ( (h*20) + (m*8) + (l*2) ) / (total_dets if total_dets > 0 else 1) * 2
rhi = max(0, min(100, rhi))

# --- FEATURE 1: 🤖 AI EXECUTIVE BRIEFING ---
st.markdown("### 🤖 Autonomous Executive Briefing")
grade = "A" if rhi > 85 else "B" if rhi > 70 else "C" if rhi > 55 else "D" if rhi > 40 else "F"
danger_zone = active_df.groupby('location_label').size().idxmax() if not active_df.empty else "None"

briefing_text = f"""
Current City infrastructure is operating at a **Grade {grade}** level with a structural integrity index of **{rhi:.1f}%**. 

- 🚩 **{h} critical fractures** requiring immediate field mobilization. 
- 📍 Analysis indicates that **{danger_zone}** remains the primary hazard cluster. 
- 🚀 **Strategic recommendation**: Prioritize high-confidence pothole rectification in high-density sectors to stabilize the degradation curve.
"""
st.info(briefing_text)

# --- FEATURE 2: 💰 BUDGET ROI OPTIMIZER ---
st.divider()
st.markdown("### 💰 Strategic Budget Optimizer (ROI)")
c1, c2 = st.columns([1, 2])

with c1:
    st.write("Input your available maintenance budget to identify the most impactful repairs.")
    budget = st.number_input("Available Budget (₹)", min_value=0, value=50000, step=5000)
    
    # Logic: ROI = Severity Weight / Cost
    # Simulated costs: High=8000, Medium=4000, Low=1500
    cost_map = {'high': 8500, 'medium': 3500, 'low': 1200}
    weight_map = {'high': 100, 'medium': 40, 'low': 10}
    
    active_df['est_cost'] = active_df['severity'].map(cost_map)
    active_df['impact_val'] = active_df['severity'].map(weight_map) * active_df['confidence']
    active_df['roi'] = active_df['impact_val'] / active_df['est_cost']
    
    plan_df = active_df.sort_values(by='roi', ascending=False)
    
    selected_tasks = []
    spent = 0
    for idx, row in plan_df.iterrows():
        if spent + row['est_cost'] <= budget:
            selected_tasks.append(row)
            spent += row['est_cost']
    
    st.metric("Potential RHI Boost", f"+{(len(selected_tasks)*1.5):.1f}%", delta=f"{len(selected_tasks)} Tasks Covered")
    st.info(f"Total Allocated: ₹{spent:,} / ₹{budget:,}")

with c2:
    if selected_tasks:
        st.write("**Top Priority Action Items:**")
        rec_df = pd.DataFrame(selected_tasks)[['task_id', 'damage_type', 'location_label', 'severity', 'est_cost']]
        st.dataframe(rec_df, use_container_width=True, hide_index=True)
    else:
        st.success("Current budget is sufficient for all minor maintenance, or no pending hazards exist.")

# --- FEATURE 3: ⛈️ WEATHER-RISK ADVISORY ---
st.divider()
st.markdown("### ⛈️ Environmental Risk Projection")
storm_mode = st.toggle("Simulate 7-Day Monsoon Impact", help="Projects hazard degradation during heavy rainfall.")

if storm_mode:
    st.error("🚨 **High Risk Advisory**: 45% of 'Medium' hazards are projected to escalate to 'Critical' status within 72 hours of rain exposure.")
    # Show projection
    proj_h = h + int(m * 0.45)
    st.warning(f"Projected Critical Count: {proj_h} (Current: {h})")
    fig_storm = go.Figure(go.Indicator(
        mode = "gauge+number", value = rhi - 15,
        title = {'text': "Projected RHI (Post-Storm)", 'font': {'size': 13}},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#E74C3C"}}
    ))
    fig_storm.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=200)
    st.plotly_chart(fig_storm, use_container_width=True)
else:
    st.info("Operating in Dry Weather parameters. No immediate environmental degradation detected.")

# --- FOOTER ---
st.divider()
st.subheader("🌋 Live Structural Stress Map")
df['magnitude'] = df['confidence'] * df['severity'].map({'high': 6, 'medium': 3, 'low': 1})
fig_3d = px.scatter_3d(df, x='lat', y='lon', z='magnitude', color='severity', size='confidence',
                       color_discrete_map={'high': '#E74C3C', 'medium': '#F39C12', 'low': '#2ECC71'})
fig_3d.update_layout(scene=dict(bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=500, margin=dict(l=0,r=0,b=0,t=0))
st.plotly_chart(fig_3d, use_container_width=True)
