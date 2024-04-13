import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load the model
loaded_model = load_model('C:\\Users\\asus\\Desktop\\cancer new\\cancermodel.h5')
print("Model loaded successfully!")

# Assuming 'img_path' is the path to your input image
img_path = 'C:\\Users\\asus\\Desktop\\cancer new\\input.jpg'  
img = image.load_img(img_path, target_size=(224, 224))  # Adjusts target_size as needed
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0  # Normalize pixel values

# Make a prediction
predictions = loaded_model.predict(img_array)

# Assuming binary classification, you can use a threshold
threshold = 0.2
if predictions[0, 0] > threshold:
    result = "Cancer Detected"
    # Display the result
    print("Prediction Result:", result)

    # Load the original image
    original_img = cv2.imread(img_path)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    # Assuming you have a way to get the coordinates of affected regions
    # You might need a more advanced method or annotation data for accurate marking
    affected_regions_coordinates = [(50, 50, 150, 150)]  # Example coordinates (x1, y1, x2, y2)

    # Mark the affected regions on the original image
    for (x1, y1, x2, y2) in affected_regions_coordinates:
        cv2.rectangle(original_img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Assuming blue rectangles

   

    # Display the raw probability score
    print("Raw Probability Score:", predictions[0, 0])

    # Assuming you want the percentage, you can convert the probability to a percentage
    percentage_affected = predictions[0, 0] * 100
    print("Percentage of Cells Affected:", percentage_affected, "%")

    # Determine the stage based on the percentage
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

    print("Cancer Stage:", stage)

     # Display the original image with marked regions
    plt.imshow(original_img)
    plt.title("Original Image with Marked Regions")
    plt.show()

else:
    result = "Cancer not Detected"
    # Display the result
    print("Prediction Result:", result)


