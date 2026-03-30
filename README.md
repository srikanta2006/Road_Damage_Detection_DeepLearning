# 🚧 Smart Road Infrastructure Management System (SRIMS)

This advanced AI-driven platform is designed to transform road safety and infrastructure maintenance. Beyond simple detection, SRIMS provides actionable intelligence through automated surveys, cost analysis, and geospatial mapping.

## ✨ New "Stand Out" Features

### 📊 AI Road Analytics Dashboard
- **Aggregate Metrics**: Real-time summary of total damages, average confidence, and primary risks.
- **Visual Intelligence**: Interactive Plotly charts for damage distribution and source analysis.
- **Maintenance Priority**: Automated ranking of repairs by cost and severity.

### 🌍 Geospatial Damage Mapping
- **Interactive Intelligence**: High-fidelity map with Folium integration.
- **Heatmap Visualization**: Identify high-density damage zones (hotspots) at a glance.
- **Survey Traces**: Track precisely where the UAV has inspected.

### 🍱 Premium UI/UX
- **Glassmorphism Design**: Modern, semi-transparent interface for a professional review feel.
- **Automated Reporting**: Real-time "toasts" and metrics that sync across all modules.

---

## Performing Detection Using Image
![Detection using image](resource/RDD_Image_Example.gif)

## Performing Detection Using Video
![Detection using video](resource/RDD_Video_Example.gif)

The project is powered by YOLOv8 deep learning model that trained on Crowdsensing-based Road Damage Detection Challenge 2022 dataset.

There is four types of damage that this model can detects such as:
- Longitudinal Crack
- Transverse Crack
- Alligator Crack
- Potholes

## Running on Local Server

... (Remaining installation steps)

## Web Demo

### [🎈Webserver Online Demo](https://roaddamagedetection.streamlit.app/)
    
    You can access the webserver demo on the streamlit cloud. But due to hardware limitations, some functions may not be working as intended. Such as, the realtime detection cannot capture the webcam input and slow inference on video detection.

## Training

### Prepare the Dataset

Download the datasets from this [github](https://github.com/sekilab/RoadDamageDetector) and you can extract the *RDD2022.zip* files into this structure.

```
/home/oracl4/project/rdd/dataset/RDD2022/
├── RDD2022_all_countries
│   ├── China_Drone
│   │   └── train
│   │       ├── annotations
│   │       │   └── xmls
│   │       ├── images
│   │       └── labels # Created after prepare dataset process
│   ├── China_MotorBike
│   │   └── ...
│   ├── Czech
│   │   └── ...
│   ├── India
│   │   └── ...
│   ├── Japan
│   │   └── ...
│   ├── Norway
│   │   └── ...
│   └── United_States
│       └── ...
└── rawData # Not Used, .zip folder
```

Perform the dataset conversion from PascalVOC to YOLOv8 format using **0_PrepareDatasetYOLOv8.ipnb** notebook. This will also create a train and val split for the dataset due to lack of test labels on the original dataset. It will also remove excess background image from the dataset. It will copy the dataset and create a new directory on the training folder.

```
├── dataset
│   └── rddJapanIndiaFiltered
│       ├── India
│       │   ├── images
│       │   │   ├── train
│       │   │   └── val
│       │   └── labels
│       │       ├── train
│       │       └── val
│       ├── Japan
│       │   └── ...
│       └── rdd_JapanIndia.yaml # Create this file for YOLO dataset config
└── runs
```

Run the training on **1_TrainingYOLOv8.ipynb** notebook. You can change the hyperparamter and training configuration on that notebook.

## Evaluation Result

This is the training result of the YOLOv8s model that trained on the filtered Japan and India dataset with RTX2060 GPU. You can perform the evaluation on your dataset with **2_EvaluationTesting.ipynb** notebook, just convert your dataset into ultralytics format.

<p align="center">
    <img src='resource/PR_curve.png' width='80%'>
    <img src='resource/confusion_matrix.png' width='80%'>
    <img src='resource/val_batch2_pred.jpg' width='100%'>
</p>

## License and Citations
- Road Damage Dataset from Crowdsensing-based Road Damage Detection Challenge (CRDDC2022)
- All rights reserved on YOLOv8 license permits by [Ultralytics](https://github.com/ultralytics/ultralytics) and [Streamlit](https://streamlit.io/) framework

---
This project is created for the [Road Damage Detection Challenge](https://s.id/RDDHariJalan23) by [Ministry of Public Works and Housing](https://pu.go.id/) for celebrating the "Peringatan Hari Jalan 2023"