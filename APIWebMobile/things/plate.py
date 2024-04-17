from roboflow import Roboflow
import pytesseract
from PIL import Image
import numpy as np
import cv2
import string
import easyocr

reader = easyocr.Reader(['en'], gpu=False)
# Specify the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Roboflow model
rf = Roboflow(api_key="Q5w8ItvZkh3JcwKZ1Dku")
project = rf.workspace().project("license-plate-recognition-rxg4e")
model = project.version(4).model

# Perform inference on a local image
result = model.predict("new1.jpg", confidence=40, overlap=30).json()

# Load the image once to avoid reloading it in the loop
image = Image.open("new1.jpg")  # Load the image using PIL
image_cv = np.array(image)  # Convert PIL image to an array for OpenCV processing
image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)  # Convert from RGB (PIL) to BGR (OpenCV)

# Process and analyze predictions
for prediction in result['predictions']:
    # Calculate the bounding box coordinates, ensuring they are integers
    x1 = int(prediction['x'] - prediction['width'] / 2)
    y1 = int(prediction['y'] - prediction['height'] / 2)
    x2 = int(prediction['x'] + prediction['width'] / 2)
    y2 = int(prediction['y'] + prediction['height'] / 2)

    # Ensure coordinates stay within the image bounds
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(image_cv.shape[1], x2), min(image_cv.shape[0], y2)

    # Crop the detected license plate area using OpenCV
    cropped_image = image_cv[y1:y2, x1:x2]

    # Convert to grayscale
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to get a binary image
    _, binary_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY_INV)

    # Optional: apply a slight blur to smooth the image
    blurred_image = cv2.GaussianBlur(binary_image, (3, 3), 0)

    # Optional: dilate the image to make characters a bit thicker
    kernel = np.ones((2, 2), np.uint8)
    dilated_image = cv2.dilate(blurred_image, kernel, iterations=1)

    # Invert image color so text is black on white background, which is preferred for OCR
    inverted_image = cv2.bitwise_not(dilated_image)

    # Convert back to PIL image for Tesseract OCR
    processed_image = Image.fromarray(inverted_image)
    processed_image.save("processed2.jpg")
    # Set Tesseract to recognize single line text
    custom_config = r'--oem 3 --psm 13'
    detections = reader.readtext(inverted_image)
    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')
    #text = pytesseract.image_to_string(processed_image, config=custom_config)

    print("Detected License Plate Number:", detections)
