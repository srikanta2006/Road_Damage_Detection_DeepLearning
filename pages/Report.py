import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

st.set_page_config(page_title="AI Report Generator", layout="centered")

st.title("📄 AI Damage Analysis Report")

# Load data
try:
    df = pd.read_csv("gps_log.csv")
except:
    st.warning("No geospatial data found. Please run a detection first!")
    st.stop()

if df.empty:
    st.warning("Spatial database is empty.")
    st.stop()

st.markdown("""
### 📋 Strategic Intelligence Report
Generate a comprehensive technical audit including severity distribution, classification metrics, and automated maintenance recommendations.
""")

# -----------------------
# 🔹 GENERATE REPORT
# -----------------------
if st.button("🚀 Compile & Generate Detailed Report", use_container_width=True):

    # Process Stats
    total_hazards = len(df)
    severity_counts = df['severity'].value_counts()
    type_counts = df['damage_type'].value_counts()
    high_risk_count = severity_counts.get('high', 0)
    
    # Recommendation Logic
    if high_risk_count > 5:
        status = "CRITICAL"
        rec = "Immediate emergency response required at logged coordinates. High density of critical risk hazards detected."
    elif high_risk_count > 0 or total_hazards > 15:
        status = "CAUTION"
        rec = "Scheduled maintenance suggested within 15 days. Monitor high-severity zones closely."
    else:
        status = "STABLE"
        rec = "Routine maintenance cycle. No immediate critical failures detected."

    pdf = FPDF()
    pdf.add_page()

    # --- Header Banner ---
    pdf.set_fill_color(26, 28, 44)
    pdf.rect(0, 0, 210, 45, 'F')
    
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(200, 25, "SRIMS Technical Damage Audit", ln=True, align='C')
    
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')

    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)

    # --- 1. Executive Intelligence Summary ---
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(200, 10, " 1. EXECUTIVE SUMMARY", ln=True, fill=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=12)

    pdf.cell(100, 10, f"Total Hazards Logged: {total_hazards}")
    pdf.cell(100, 10, f"Infrastructure Status: {status}", ln=True)
    pdf.cell(100, 10, f"Primary Damage: {df['damage_type'].mode()[0]}")
    pdf.cell(100, 10, f"Avg Confidence: {round(df['confidence'].mean(), 2)}", ln=True)

    pdf.ln(10)

    # --- 2. Distribution Data ---
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, " 2. STATISTICAL DISTRIBUTION", ln=True, fill=True)
    pdf.ln(5)
    
    col_width = 95
    pdf.set_font("Arial", "B", 11)
    pdf.cell(col_width, 10, "Classification Breakdown", 0)
    pdf.cell(col_width, 10, "Severity Breakdown", 1)
    
    pdf.set_font("Arial", size=10)
    # Combine lists to iterate through counts
    max_rows = max(len(type_counts), len(severity_counts))
    type_idx = type_counts.index.tolist()
    sev_idx = severity_counts.index.tolist()
    
    for i in range(max_rows):
        t_text = f"{type_idx[i]}: {type_counts[type_idx[i]]}" if i < len(type_idx) else ""
        s_text = f"{sev_idx[i]}: {severity_counts[sev_idx[i]]}" if i < len(sev_idx) else ""
        pdf.cell(col_width, 8, t_text)
        pdf.cell(col_width, 8, s_text) # Removed boundary box here for cleaner look or could add 1
        pdf.ln()
    
    pdf.ln(10)

    # --- 3. Maintenance Recommendations ---
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, " 3. STRATEGIC RECOMMENDATIONS", ln=True, fill=True)
    pdf.ln(5)
    pdf.set_font("Arial", "I", 11)
    pdf.multi_cell(190, 8, rec)

    pdf.ln(10)

    # --- 4. Detailed Audit Entries ---
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, " 4. DETAILED HAZARD AUDIT", ln=True, fill=True)
    pdf.ln(5)

    # Table Header
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(75, 10, "Classification", 1, 0, 'C', True)
    pdf.cell(40, 10, "Confidence", 1, 0, 'C', True)
    pdf.cell(40, 10, "Severity", 1, 0, 'C', True)
    pdf.cell(35, 10, "Location", 1, 1, 'C', True)

    # Table Data
    pdf.set_font("Arial", size=9)
    for _, row in df.iterrows():
        # Truncate location label for table fit
        loc = str(row['location_label'])[:15]
        pdf.cell(75, 9, str(row['damage_type']), 1)
        pdf.cell(40, 9, f"{row['confidence']:.2%}", 1, 0, 'R')
        pdf.cell(40, 9, str(row['severity']).upper(), 1, 0, 'C')
        pdf.cell(35, 9, loc, 1, 1, 'C')

    # Save file
    file_path = "road_report.pdf"
    pdf.output(file_path)

    # Interactive Download Section
    st.divider()
    with open(file_path, "rb") as f:
        st.download_button(
            "⬇ Download Strategic Audit PDF",
            f,
            file_name=f"SRIMS_Audit_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # Cleanup temporary local file
    if os.path.exists(file_path):
        os.remove(file_path)