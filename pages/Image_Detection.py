import logging
from pathlib import Path
from typing import NamedTuple
import time
import csv
import os
import random
from streamlit_image_comparison import image_comparison

import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
from sample_utils.download import download_file

from utils.alerts import render_sidebar_alerts

st.set_page_config(
    page_title="Image Detection",
    page_icon="📷",
    layout="wide"
)

render_sidebar_alerts()

# Custom Styling
st.markdown("""
<style>
.main { background-color: #0E1117; }
h1 { color: white; text-align: center; }
.stButton>button { background-color: #FF4B4B; color: white; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

import uuid

def log_detection(filename, lat, lon, label, damage_type, confidence, media_type):
    severity = "high" if confidence >= 0.8 else "medium" if confidence >= 0.5 else "low"
    task_id = str(uuid.uuid4())[:8]
    row = [filename, lat, lon, label, damage_type, round(confidence, 2), severity, media_type, "Pending", task_id]
    with open("gps_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

HERE = Path(__file__).parent
ROOT = HERE.parent

MODEL_URL = "https://github.com/oracl4/RoadDamageDetection/raw/main/models/YOLOv8_Small_RDD.pt"
MODEL_LOCAL_PATH = ROOT / "./models/YOLOv8_Small_RDD.pt"
download_file(MODEL_URL, MODEL_LOCAL_PATH, expected_size=89569358)

if "model" not in st.session_state:
    st.session_state.model = YOLO(MODEL_LOCAL_PATH)

net = st.session_state.model
CLASSES = ["Longitudinal Crack", "Transverse Crack", "Alligator Crack", "Potholes"]

st.title("🖼️ Image Road Damage Detection")

col_menu_1, col_menu_2 = st.columns([2, 1])

with col_menu_1:
    image_file = st.file_uploader("Upload Image", type=['png', 'jpg'])
    score_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.3, 0.05)

with col_menu_2:
    st.subheader("📍 Location Settings")
    lat_val = st.number_input("Latitude", value=17.3850, format="%.4f")
    lon_val = st.number_input("Longitude", value=78.4867, format="%.4f")
    location_label = st.text_input("Location Label", value="Hyderabad")

st.divider()

if image_file:
    image = Image.open(image_file)
    _image = np.array(image)

    resized = cv2.resize(_image, (640, 640))
    results = net.predict(resized, conf=score_threshold)

    rhi = 100
    cost = 0

    # ✅ RESET LOG FOR NEW IMAGE RUN
    header = ["filename","lat","lon","location_label","damage_type","confidence","severity","media_type","status","task_id"]
    with open("gps_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

    if len(results[0].boxes) > 0:
        for r in results:
            for b in r.boxes.cpu().numpy():
                cls = int(b.cls[0])
                conf = float(b.conf[0])
                x1, y1, x2, y2 = b.xyxy[0]
                area = (x2 - x1) * (y2 - y1) / 1000

                if cls == 3: # Pothole
                    if area < 5: c, impact = 1500, 8
                    elif area < 15: c, impact = 4000, 15
                    else: c, impact = 8000, 25
                else: # Crack
                    if area < 5: c, impact = 500, 3
                    elif area < 15: c, impact = 1500, 6
                    else: c, impact = 3000, 10

                cost += c
                rhi -= impact
                
                # ✅ LOCALIZED MAPPING JITTER (±10 meters)
                jitter_lat = lat_val + random.uniform(-0.0001, 0.0001)
                jitter_lon = lon_val + random.uniform(-0.0001, 0.0001)

                log_detection(
                    image_file.name, 
                    jitter_lat, jitter_lon, 
                    location_label, 
                    CLASSES[cls], 
                    conf, 
                    "image"
                )

        rhi = max(rhi, 0)
        m1, m2 = st.columns(2)
        m1.metric("Road Health Index", int(rhi))
        m2.metric("Repair Cost", f"₹{int(cost)}")
    else:
        st.success("No road damage detected!")

    st.divider()

    annotated = results[0].plot()
    annotated = cv2.resize(annotated, (_image.shape[1], _image.shape[0]))
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    st.subheader("🔍 Interactive Damage Comparison")
    
    # PREMIUM FEATURE: Image Comparison Slider
    image_comparison(
        img1=Image.fromarray(_image),
        img2=Image.fromarray(annotated_rgb),
        label1="Original",
        label2="Detected Damages",
        width=None,
        make_responsive=True,
        starting_position=50,
        show_labels=True
    )

    st.divider()

    col_btn = st.columns([1, 1, 1])
    with col_btn[1]:
        buffer = BytesIO()
        Image.fromarray(annotated_rgb).save(buffer, format="PNG")
        st.download_button(
            "⬇ Download High-Res Result",
            buffer.getvalue(),
            file_name="RDD_Result.png",
            mime="image/png",
            use_container_width=True
        )
    
    if len(results[0].boxes) > 0:
        st.toast(f"✅ {len(results[0].boxes)} damages logged to dashboard!")
