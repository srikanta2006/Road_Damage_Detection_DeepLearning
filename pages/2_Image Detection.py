import logging
from pathlib import Path
from typing import NamedTuple

import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
from sample_utils.download import download_file

st.set_page_config(
    page_title="Image Detection",
    page_icon="📷",
    layout="wide"
)

# ✅ CLEAN CSS (NO METRIC OVERRIDE)
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    color: white;
    text-align: center;
}

.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

HERE = Path(__file__).parent
ROOT = HERE.parent

MODEL_URL = "https://github.com/oracl4/RoadDamageDetection/raw/main/models/YOLOv8_Small_RDD.pt"
MODEL_LOCAL_PATH = ROOT / "./models/YOLOv8_Small_RDD.pt"
download_file(MODEL_URL, MODEL_LOCAL_PATH, expected_size=89569358)

if "model" not in st.session_state:
    st.session_state.model = YOLO(MODEL_LOCAL_PATH)

net = st.session_state.model

st.title("🖼️ Image Road Damage Detection")

# ✅ uploader first
image_file = st.file_uploader("Upload Image", type=['png', 'jpg'])

# ✅ slider below
score_threshold = st.slider(
    "Confidence Threshold",
    0.0, 1.0, 0.3, 0.05
)

st.divider()

if image_file:

    image = Image.open(image_file)
    _image = np.array(image)

    resized = cv2.resize(_image, (640, 640))
    results = net.predict(resized, conf=score_threshold)

    rhi = 100
    cost = 0

    for r in results:
        for b in r.boxes.cpu().numpy():
            cls = int(b.cls[0])
            x1, y1, x2, y2 = b.xyxy[0]
            area = (x2 - x1) * (y2 - y1) / 1000

            if cls == 3:
                if area < 5:
                    c, impact = 1500, 8
                elif area < 15:
                    c, impact = 4000, 15
                else:
                    c, impact = 8000, 25
            else:
                if area < 5:
                    c, impact = 500, 3
                elif area < 15:
                    c, impact = 1500, 6
                else:
                    c, impact = 3000, 10

            cost += c
            rhi -= impact

    rhi = max(rhi, 0)

    # ✅ CLEAN metrics (default streamlit style)
    m1, m2 = st.columns(2)
    m1.metric("Road Health Index", rhi)
    m2.metric("Repair Cost", f"₹{cost}")

    st.divider()

    annotated = results[0].plot()
    annotated = cv2.resize(annotated, (_image.shape[1], _image.shape[0]))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(_image, use_container_width=True)

    with col2:
        st.subheader("Prediction")
        st.image(annotated, use_container_width=True)

        buffer = BytesIO()
        Image.fromarray(annotated).save(buffer, format="PNG")

        st.download_button(
            "Download Result",
            buffer.getvalue(),
            file_name="RDD_Result.png",
            mime="image/png"
        )
