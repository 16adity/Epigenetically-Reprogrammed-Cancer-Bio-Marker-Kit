import os
import base64
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from io import BytesIO

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the model file
model_path = os.path.join(current_dir, 'cancermodel.h5')

# Load the model
loaded_model = load_model(model_path)
print("Model loaded successfully!")

def predict_cancer(file_storage):
    # Process the uploaded image
    file_data = np.frombuffer(file_storage.read(), np.uint8)
    img = cv2.imdecode(file_data, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))

    img_array = np.expand_dims(img, axis=0)
    img_array = img_array / 255.0  # Normalize pixel values

    # Make a prediction
    predictions = loaded_model.predict(img_array)

    # Assuming binary classification, you can use a threshold
    threshold = 0.2
    if predictions[0, 0] > threshold:
        result = "Cancer Cells Detected"
    else:
        result = "No Cancer Cells Detected"

    # Convert the image to a base64 string
    _, buffer = cv2.imencode('.jpg', img)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Calculate the percentage of affected cells
    percentage_affected = predictions[0, 0] * 100

    # Determine the cancer stage based on the percentage
    if percentage_affected < 20:
        stage = "Stage 1"
    elif 20 <= percentage_affected < 40:
        stage = "Stage 2"
    elif 40 <= percentage_affected < 60:
        stage = "Stage 3"
    elif 60 <= percentage_affected < 80:
        stage = "Stage 4"
    else:
        stage = "Stage 5"

    return result, percentage_affected, stage, image_base64
