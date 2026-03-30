import streamlit as st
import pandas as pd
import os
import time

def render_sidebar_alerts():
    if not os.path.exists("gps_log.csv"):
        return

    df = pd.read_csv("gps_log.csv")
    if df.empty:
        return

    # Critical Alerts (High Severity & NOT Resolved)
    critical_alerts = df[(df['severity'] == 'high') & (df['status'] != 'Resolved')]

    with st.sidebar:
        st.divider()
        st.markdown("### 🔔 Operational Alerts")
        
        if len(critical_alerts) == 0:
            st.success("✅ No critical hazards pending.")
        else:
            st.error(f"⚠️ {len(critical_alerts)} Critical Hazards detected!")
            
            for idx, row in critical_alerts.head(5).iterrows():
                with st.expander(f"🔴 {row['damage_type']} at {row['location_label']}"):
                    st.write(f"**Task ID:** `{row['task_id']}`")
                    st.write(f"**Confidence:** {row['confidence']:.1%}")
                    if st.button("Direct to Management", key=f"alert_{row['task_id']}"):
                        st.toast(f"Redirecting to Task {row['task_id']}...")
                        time.sleep(0.5)
                        st.switch_page("pages/6_Management.py")
        
        st.divider()
