import os
from datetime import time

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Form
from fastapi.responses import JSONResponse
import uvicorn
from PIL import Image
import numpy as np
import cv2
import io
import easyocr
from roboflow import Roboflow

from src.dynamoDB_interaction import get_table
from src.notification import notify_user

# Initialize EasyOCR and Roboflow
reader = easyocr.Reader(['en'], gpu=False)

rf = Roboflow(api_key="mHJlgEyKpwOZChzaVqFi")
project = rf.workspace().project("licence-plate-dausq")
model = project.version(2).model

plate_router = APIRouter(prefix="/plate", tags=["Plate Recognition"])

@plate_router.post("/upload/")
async def recognize_plate(file: UploadFile = File(...), spot_id: int = Form(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image_cv = np.array(image)  # Convert PIL image to an array for OpenCV processing
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)  # Convert from RGB (PIL) to BGR (OpenCV)

    try:
        # Perform inference to find license plates
        results = model.predict(image_cv, confidence=40, overlap=30).json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during plate recognition: {str(e)}")

    plates = process_image_for_plate_recognition(image_cv, results['predictions'])

    for plate_number in plates:
        reservation = verify_plate_with_reservations(plate_number, spot_id)

        if reservation and reservation['status'] == 'invalid':
            notify_user(reservation['user_id'], plate_number)
            return JSONResponse(content={"message": "Mismatched plate, user notified", "plate": plate_number})

    return JSONResponse(content={"message": "Plate verified", "plates": plates})


def process_image_for_plate_recognition(image_cv, predictions):
    detected_plates = []
    for prediction in predictions:
        x_center = prediction['x']
        y_center = prediction['y']
        width = prediction['width']
        height = prediction['height']

        # Calculate the bounding box coordinates
        x1 = int(x_center - width / 2)
        y1 = int(y_center - height / 2)
        x2 = int(x_center + width / 2)
        y2 = int(y_center + height / 2)

        # Ensure the coordinates are within the image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image_cv.shape[1], x2)
        y2 = min(image_cv.shape[0], y2)

        # Draw the bounding box on the original image for verification
        image_with_box = image_cv.copy()
        cv2.rectangle(image_with_box, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imwrite("image_with_box.jpg", image_with_box)

        # Crop the detected license plate area
        cropped_image = image_cv[y1:y2, x1:x2]
        cv2.imwrite("cropped.jpg", cropped_image)

        detections = reader.readtext(cropped_image)
        print(detections)
        for bbox, text, score in detections:
            if score > 0.1:  # Only consider detections with high confidence
                detected_plates.append(text)

    return detected_plates


def verify_plate_with_reservations(plate_number: str, spot_id: int) -> dict:
    table = get_table("Reservations")

    for _ in range(5):  # Retry up to 5 times
        try:
            # Query DynamoDB using the GSI for the reservation based on the spot ID
            response = table.query(
                IndexName='SpotIndex',  # Use the name of your GSI
                KeyConditionExpression=Key('spot_id').eq(str(spot_id))
            )

            items = response.get('Items', [])
            if not items:
                return {'status': 'invalid'}

            for item in items:
                if item['license_plate'] == plate_number:
                    return {'status': 'valid'}
                else:
                    print(item['user_id'])
                    return {'status': 'invalid', 'user_id': item['user_id']}

        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException' and 'Cannot read from backfilling' in \
                    e.response['Error']['Message']:
                time.sleep(10)  # Wait for 10 seconds before retrying
            else:
                raise e

    return {'status': 'invalid'}

