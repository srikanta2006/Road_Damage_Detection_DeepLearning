import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from utils.alerts import render_sidebar_alerts

st.set_page_config(page_title="Strategic Map", page_icon="🗺️", layout="wide")

render_sidebar_alerts()

# PREMIUM GLASSMORPHISM THEME
st.markdown("""
<style>
.main { background: radial-gradient(circle at top right, #1a1c2c, #0E1117); }
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 20px;
    margin-bottom: 20px;
    text-align: center;
}
.stat-value { font-size: 28px; font-weight: 800; color: #FF4B4B; text-shadow: 0 0 10px rgba(255,75,75,0.3); }
.stat-label { font-size: 14px; color: #aaa; text-transform: uppercase; letter-spacing: 1.5px; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 Strategic Damage Geospatial Hub")

# Load Data
try:
    df = pd.read_csv("gps_log.csv")
except:
    st.warning("No GPS data found. Run a detection to populate the map!")
    st.stop()

if df.empty:
    st.warning("The spatial database is currently empty.")
    st.stop()

# --- SIDEBAR: ADVANCED INTELLIGENCE FILTERS ---
st.sidebar.header("🛠️ Intelligence Filters")

selected_types = st.sidebar.multiselect(
    "Damage Classification",
    options=df['damage_type'].unique(),
    default=df['damage_type'].unique()
)

selected_status = st.sidebar.multiselect(
    "Maintenance Status",
    options=df['status'].unique(),
    default=df['status'].unique()
)

min_conf = st.sidebar.select_slider(
    "Trust Threshold (Confidence)",
    options=[round(i*0.1, 1) for i in range(11)],
    value=0.0
)

# Apply Filters
filtered_df = df[
    (df['damage_type'].isin(selected_types)) &
    (df['status'].isin(selected_status)) &
    (df['confidence'] >= min_conf)
]

# --- EXECUTIVE SUMMARY METRICS ---
m1, m2, m3, m4 = st.columns(4)

pending_count = len(filtered_df[filtered_df['status'] == 'Pending'])
high_severity = len(filtered_df[filtered_df['severity'] == 'high'])
most_common = filtered_df['damage_type'].mode()[0] if not filtered_df.empty else "N/A"
avg_conf = filtered_df['confidence'].mean() if not filtered_df.empty else 0

with m1:
    st.markdown(f"<div class='glass-card'><div class='stat-label'>Pending Hazards</div><div class='stat-value'>{pending_count}</div></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='glass-card'><div class='stat-label'>Critical Risks</div><div class='stat-value'>{high_severity}</div></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='glass-card'><div class='stat-label'>Primary Mode</div><div class='stat-value'>{most_common}</div></div>", unsafe_allow_html=True)
with m4:
    st.markdown(f"<div class='glass-card'><div class='stat-label'>Mean Accuracy</div><div class='stat-value'>{avg_conf:.1%}</div></div>", unsafe_allow_html=True)

# --- GEOSPATIAL ENGINE ---
if not filtered_df.empty:
    center_lat = filtered_df['lat'].mean()
    center_lon = filtered_df['lon'].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="CartoDB dark_matter")
    
    # Layer Groups
    marker_layer = folium.FeatureGroup(name="Pin Detections").add_to(m)
    heat_layer = folium.FeatureGroup(name="Density Heatmap", show=False).add_to(m)

    # 🔹 Markers
    for _, row in filtered_df.iterrows():
        # Color Logic: Status based
        if row['status'] == 'Resolved':
            color = "#2ECC71" # Emerald Green
            icon = "check"
        elif row['status'] == 'In Progress':
            color = "#3498DB" # Bright Blue
            icon = "refresh"
        else:
            color = "#FF4B4B" if row['severity'] == 'high' else "#FFA500"
            icon = "exclamation"
        
        popup_html = f"""
        <div style='font-family: sans-serif; min-width: 180px;'>
            <h4 style='margin:0; color:#333;'>{row['damage_type']}</h4>
            <p style='color:gray; font-size:10px;'>Task ID: {row['task_id']}</p>
            <hr style='margin:8px 0;'>
            <p><b>Status:</b> <span style='color:{color}; font-weight:bold;'>{row['status'].upper()}</span></p>
            <p><b>Severity:</b> {row['severity'].upper()}</p>
            <p><b>Confidence:</b> {row['confidence']:.2%}</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=9,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(marker_layer)

    # 🔹 Heatmap
    heat_data = filtered_df[['lat', 'lon']].values.tolist()
    HeatMap(heat_data, radius=15, blur=10).add_to(heat_layer)
    
    folium.LayerControl().add_to(m)
    
    # Render with Streamlit
    st_folium(m, use_container_width=True, height=600)
else:
    st.info("No data points match current filter criteria.")

# --- DATA EXPLORER ---
with st.expander("📊 View Detailed Spatial Logs"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "confidence": st.column_config.ProgressColumn("Accuracy", min_value=0, max_value=1),
            "media_type": "Source"
        }
    )