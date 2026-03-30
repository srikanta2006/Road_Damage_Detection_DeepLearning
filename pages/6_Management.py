import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.alerts import render_sidebar_alerts

st.set_page_config(page_title="Management Portal", page_icon="🏢", layout="wide")

render_sidebar_alerts()

# PREMIUM GLASSMORPHISM THEME
st.markdown("""
<style>
.main { background: radial-gradient(circle at bottom left, #1a1c2c, #0E1117); }
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 25px;
    margin-bottom: 20px;
}
.role-badge {
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
}
.official { background: #4B79FF; color: white; }
.engineer { background: #FF9F4B; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🏢 SRIMS Management & Collaboration")

# Load Data
def load_data():
    if os.path.exists("gps_log.csv"):
        return pd.read_csv("gps_log.csv")
    return pd.DataFrame()

def save_data(df):
    df.to_csv("gps_log.csv", index=False)

df = load_data()

if df.empty:
    st.warning("No operational data available. Please run detections first.")
    st.stop()

# --- SIDEBAR: ROLE SELECTION ---
st.sidebar.header("🔐 Access Control")
role = st.sidebar.radio("Connect as:", ["Strategic Official", "Field Engineer"])

if role == "Strategic Official":
    st.sidebar.markdown("<span class='role-badge official'>Official Access</span>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<span class='role-badge engineer'>Engineer Access</span>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🔹 VIEW 1: STRATEGIC OFFICIAL (Executive Dashboard)
# ---------------------------------------------------------
if role == "Strategic Official":
    st.subheader("📊 Executive Oversight")
    
    col1, col2, col3 = st.columns(3)
    
    pending = len(df[df['status'] != 'Resolved'])
    resolved = len(df[df['status'] == 'Resolved'])
    # Simulated Budget Logic
    est_cost = pending * 2500 # Avg repair cost
    
    with col1:
        st.markdown(f"<div class='glass-card'><h3>{pending}</h3><p>Active Hazards</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='glass-card'><h3>{resolved}</h3><p>Rectified Assets</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='glass-card'><h3>₹{est_cost:,}</h3><p>Maintenance Liability</p></div>", unsafe_allow_html=True)

    st.divider()
    
    # Quick Rectification Table
    st.markdown("### 📋 Quick Rectification Audit")
    p_df = df[df['status'] != 'Resolved'].copy()
    if p_df.empty:
        st.success("Infrastructure Integrity: 100%. No pending actions.")
    else:
        for i, row in p_df.head(5).iterrows():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"**{row['damage_type']}** @ {row['location_label']} (`{row['task_id']}`)")
            with c2:
                st.write(f"Status: `{row['status']}`")
            with c3:
                if st.button("Mark Rectified ✅", key=f"rec_off_{row['task_id']}"):
                    idx = df[df['task_id'] == row['task_id']].index
                    df.at[idx[0], 'status'] = 'Resolved'
                    save_data(df)
                    st.toast(f"Task {row['task_id']} officially Rectified.")
                    st.rerun()

# ---------------------------------------------------------
# 🔹 VIEW 2: FIELD ENGINEER (One-Click Operations)
# ---------------------------------------------------------
else:
    st.subheader("🛠️ Operational Maintenance List")
    
    # Priority Sorting Logic
    severity_map = {"high": 3, "medium": 2, "low": 1}
    df['prio_val'] = df['severity'].map(severity_map)
    df = df.sort_values(by=['prio_val', 'confidence'], ascending=False)

    worklist = df[df['status'] != 'Resolved'].copy()

    if worklist.empty:
        st.balloons()
        st.success("All assigned tasks are finished. Database is clear!")
    else:
        # Display Tasks with Action Buttons
        for idx, row in worklist.iterrows():
            with st.expander(f"Task {row['task_id']} | {row['damage_type']} ({row['severity'].upper()})"):
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.write(f"**Coords:** {row['lat']:.4f}, {row['lon']:.4f} | **Source:** {row['filename']}")
                    st.write(f"**Status:** {row['status']}")
                
                with c2:
                    if st.button(f"Mark Finished ✅", key=f"fin_{row['task_id']}", use_container_width=True):
                        idx_orig = df[df['task_id'] == row['task_id']].index
                        df.at[idx_orig[0], 'status'] = "Resolved"
                        save_data(df.drop(columns=['prio_val']))
                        st.toast(f"✅ Hazard {row['task_id']} successfully rectified.")
                        st.rerun()

st.divider()
st.subheader("🗂️ Master Strategic Audit")
st.dataframe(df.drop(columns=['prio_val'] if 'prio_val' in df.columns else []), use_container_width=True)
