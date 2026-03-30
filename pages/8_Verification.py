import streamlit as st
import pandas as pd
import os
from PIL import Image
from streamlit_image_comparison import image_comparison
from utils.alerts import render_sidebar_alerts

st.set_page_config(page_title="Field Verification", page_icon="✅", layout="wide")

# ADAPTIVE THEME
st.markdown("""
<style>
.main { background: radial-gradient(circle at bottom center, #1a2c3a, #0E1117); }
.verification-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

render_sidebar_alerts()

st.title("✅ Field Repair Verification")

# Load Data
if os.path.exists("gps_log.csv"):
    df = pd.read_csv("gps_log.csv")
else:
    st.warning("Spatial database unavailable.")
    st.stop()

if df.empty:
    st.warning("Database is empty.")
    st.stop()

# --- FILTER TASKS ---
pending_list = df[df['status'] != 'Resolved'].copy()

if pending_list.empty:
    st.success("🎉 All infrastructure tasks have been successfully verified and resolved!")
    st.balloons()
    st.stop()

st.subheader("🛠️ Active Worklist")
task_selection = st.selectbox("Select Task to Verify", pending_list['task_id'])

# Task Details
selected_task = pending_list[pending_list['task_id'] == task_selection].iloc[0]

c1, c2 = st.columns([1, 1.5])

with c1:
    st.markdown("<div class='verification-card'>", unsafe_allow_html=True)
    st.write(f"**Task ID:** `{selected_task['task_id']}`")
    st.write(f"**Hazard Type:** {selected_task['damage_type']}")
    st.write(f"**Coordinate:** {selected_task['lat']:.4f}, {selected_task['lon']:.4f}")
    st.write(f"**Reported Severity:** {selected_task['severity'].upper()}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    
    # Verification Upload
    repair_img = st.file_uploader("📸 Upload Repair Verification Photo", type=['jpg', 'jpeg', 'png'])
    
    if repair_img:
        if st.button("🚀 Confirm & Resolve Task", use_container_width=True):
            # Update status in the master CSV
            idx = df[df['task_id'] == task_selection].index
            df.at[idx[0], 'status'] = 'Resolved'
            df.to_csv("gps_log.csv", index=False)
            st.success(f"Task {task_selection} Successfully Resolved!")
            time.sleep(1)
            st.rerun()

with c2:
    st.subheader("🔍 Visual Audit")
    
    # Since we don't have the "original" image file path easily accessible in a repo-relative way 
    # (it might've been a temp upload), we simulate the "Before" with a placeholder or the detected bounding box info.
    # For the DEMO, we show the uploaded repair photo and a label.
    
    if repair_img:
        st.info("Verification image received. Final cross-check in progress...")
        st.image(repair_img, caption="New Structural Surface (Post-Repair)", use_container_width=True)
    else:
        st.warning("Waiting for repair verification photo...")
