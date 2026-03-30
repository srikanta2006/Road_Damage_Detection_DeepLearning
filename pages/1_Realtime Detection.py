import logging
import queue
from pathlib import Path
from typing import List, NamedTuple

import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from ultralytics import YOLO
from sample_utils.download import download_file
from sample_utils.get_STUNServer import getSTUNServer

st.set_page_config(page_title="Realtime Detection", page_icon="📷", layout="wide")

st.markdown("""
<style>
.main {background-color:#0E1117;}
h1 {color:white;text-align:center;}
.stButton>button {background:#FF4B4B;color:white;border-radius:8px;height:3em;width:100%;}
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

STUN_SERVER = [{"urls": ["stun:" + str(getSTUNServer())]}]

CLASSES=["Longitudinal Crack","Transverse Crack","Alligator Crack","Potholes"]

class Detection(NamedTuple):
    class_id:int
    label:str
    score:float
    box:np.ndarray

st.title("📡 Realtime Road Damage Detection")

score_threshold = st.slider("Confidence Threshold",0.0,1.0,0.5,0.05)

result_queue: "queue.Queue[List[Detection]]" = queue.Queue()

def callback(frame: av.VideoFrame):
    img=frame.to_ndarray(format="bgr24")
    res=net.predict(cv2.resize(img,(640,640)),conf=score_threshold)

    dets=[]
    for r in res:
        for b in r.boxes.cpu().numpy():
            dets.append(Detection(int(b.cls),CLASSES[int(b.cls)],float(b.conf[0]),b.xyxy[0]))

    result_queue.put(dets)

    return av.VideoFrame.from_ndarray(res[0].plot(),format="bgr24")

webrtc_streamer(
    key="rdd",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={"iceServers": STUN_SERVER},
    video_frame_callback=callback,
    media_stream_constraints={"video":True,"audio":False},
    async_processing=True
)

if st.checkbox("Show Predictions"):
    table=st.empty()
    while True:
        table.dataframe(result_queue.get(),use_container_width=True)
