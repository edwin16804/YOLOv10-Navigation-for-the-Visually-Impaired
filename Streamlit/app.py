import streamlit as st
import cv2
import torch
import numpy as np
from gtts import gTTS
import os
import tempfile

# Load the YOLO model (adjust path and model type as necessary)
model = torch.hub.load('ultralytics/yolov11', 'yolo11n')  # Change to your YOLO model

def load_image(image_file):
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    return img

def detect_objects(image):
    results = model(image)  # Perform detection
    return results

def display_results(results):
    # Extract detections
    detections = results.pandas().xyxy[0]
    detected_classes = detections['name'].values
    detected_counts = detections['confidence'].values
    return detected_classes, detected_counts

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(f"{fp.name}.mp3")
        os.system(f"start {fp.name}.mp3")  # For Windows. Use 'afplay' for macOS or 'mpg123' for Linux.

st.title("YOLO Object Detection App")
st.write("Upload an image to detect objects.")

image_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])

if image_file is not None:
    image = load_image(image_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    results = detect_objects(image)
    detected_classes, detected_counts = display_results(results)

    if len(detected_classes) > 0:
        object_summary = {obj: int(np.sum(detected_counts[detected_classes == obj])) for obj in set(detected_classes)}
        st.write("Detected Objects:")
        for obj, count in object_summary.items():
            st.write(f"{obj}: {count}")

        # Speak out the detected objects
        speak_text(", ".join([f"{count} {obj}" for obj, count in object_summary.items()]))
    else:
        st.write("No objects detected.")
