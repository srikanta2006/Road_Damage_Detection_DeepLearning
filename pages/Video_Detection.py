import os
from pathlib import Path
import cv2
import streamlit as st
import time
import csv
import random
from ultralytics import YOLO
from sample_utils.download import download_file

from utils.alerts import render_sidebar_alerts

st.set_page_config(
    page_title="Video Detection",
    page_icon="📷",
    layout="wide"
)

render_sidebar_alerts()

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
    # No need to check for file existence since we reset it at the start of the button click
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

os.makedirs("./temp", exist_ok=True)
input_path = "./temp/input.mp4"
output_path = "./temp/output.mp4"

st.title("🎥 Video Road Damage Detection")

col_menu_1, col_menu_2 = st.columns([2, 1])

with col_menu_1:
    video = st.file_uploader("Upload Video", type="mp4")
    conf = st.slider("Confidence Threshold", 0.0, 1.0, 0.3, 0.05)

with col_menu_2:
    st.subheader("📍 Location Settings")
    lat_val = st.number_input("Latitude", value=17.3850, format="%.4f")
    lon_val = st.number_input("Longitude", value=78.4867, format="%.4f")
    location_label = st.text_input("Location Label", value="Hyderabad")

st.divider()

if video and st.button("🚀 Process Video"):

    with open(input_path, "wb") as f:
        f.write(video.getbuffer())

    # ✅ RESET LOG FOR NEW VIDEO RUN
    header = ["filename","lat","lon","location_label","damage_type","confidence","severity","media_type","status","task_id"]
    with open("gps_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(5)
    total = int(cap.get(7))

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    rhi = 100
    cost = 0
    progress = st.progress(0)

    col1, col2 = st.columns(2)
    rhi_box = col1.empty()
    cost_box = col2.empty()

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process every 15th frame for performance and better sampling
        if frame_count % 15 == 0:
            resized = cv2.resize(frame, (640, 640))
            results = net.predict(resized, conf=conf, verbose=False)
            
            for r in results:
                for b in r.boxes.cpu().numpy():
                    cls = int(b.cls[0])
                    conf_score = float(b.conf[0])
                    x1, y1, x2, y2 = b.xyxy[0]
                    area = (x2 - x1) * (y2 - y1) / 1000

                    if cls == 3: # Pothole
                        if area < 5: c, impact = 1500, 5
                        elif area < 15: c, impact = 4000, 10
                        else: c, impact = 8000, 15
                    else: # Crack
                        if area < 5: c, impact = 500, 2
                        elif area < 15: c, impact = 1500, 4
                        else: c, impact = 3000, 6

                    cost += c * 0.5 # Adjustment for sampling
                    rhi -= impact
                    
                    # ✅ LOCALIZED MAPPING JITTER (±10 meters)
                    # Add jitter so markers don't stack but stay very close (same street/intersection).
                    jitter_lat = lat_val + random.uniform(-0.0001, 0.0001)
                    jitter_lon = lon_val + random.uniform(-0.0001, 0.0001)

                    # Log to CSV
                    log_detection(
                        video.name, 
                        jitter_lat, jitter_lon, 
                        location_label, 
                        CLASSES[cls], 
                        conf_score, 
                        "video"
                    )

            rhi = max(rhi, 0)
            annotated = results[0].plot()
            annotated = cv2.resize(annotated, (width, height))
            out.write(annotated)
            
            rhi_box.metric("Road Health Index", int(rhi))
            cost_box.metric("Repair Cost", f"₹{int(cost)}")
        else:
            pass

        frame_count += 1
        progress.progress(min(frame_count / total, 1.0))

    cap.release()
    out.release()

    st.success("Processing Completed")

    if os.path.exists(output_path):
        st.subheader("Processed Video")
        with open(output_path, "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes)
        st.download_button("Download Processed Video", video_bytes, file_name="output.mp4")
    
    st.toast("✅ Video analytics synced with dashboard!")
