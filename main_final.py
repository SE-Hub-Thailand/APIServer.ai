from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics import YOLO
# from PIL import Image
import io
import os
import shutil
# from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf  
from io import BytesIO

app = FastAPI()

#Bottle Model
model_bottle_size = tf.keras.models.load_model('weights/bottle_size_model.h5') 
model_bottle_brand = tf.keras.models.load_model('weights/bottle_brand_model.h5')  

bottle_size_classes = ['bottel_1600', 'bottel_350', 'bottle_1250', 'bottle_1500', 'bottle_1950', 'bottle_280', 'bottle_300', 'bottle_320', 'bottle_322', 'bottle_340', 'bottle_360', 'bottle_400', 'bottle_410', 'bottle_430', 'bottle_440', 'bottle_445', 'bottle_500', 'bottle_600ml', 'bottle_640', 'bottle_750'] 
bottle_brand_classes = ['amphawa', 'amwelplus', 'aquafina', 'beauti_drink', 'big', 'coca_cola', 'cocomax', 'crystal', 'est', 'ichitan', 'kato', 'mansome', 'mikko', 'minearlwater', 'nestle', 'no_band', 'oishi', 'pepsi', 'sing', 'spinking_water', 'sprite', 'srithep', 'tipchumporn_drinking_water'] 

#Can Model
model_can_size = tf.keras.models.load_model('weights/can_size_model.h5') 
model_can_brand = tf.keras.models.load_model('weights/can_brand_model.h5')  

can_size_classes = ['can_180', 'can_245', 'can_330', 'can_490'] 
can_brand_classes = ['birdy', 'calpis_lacto', 'chang', 'green_mate', 'leo', 'nescafe', 'sing'] 

CONFIDENCE_THRESHOLD = 0.3

def preprocess_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    image = image.resize((256, 144))  
    image = np.array(image) / 255.0  
    image = np.expand_dims(image, axis=0)  
    return image

def predict_category(image_bytes, model_size, model_brand, size_classes, brand_classes):
    processed_image = preprocess_image(image_bytes)

    size_prediction = model_size.predict(processed_image)
    size_index = np.argmax(size_prediction)  
    size_confidence = np.max(size_prediction) 

    brand_prediction = model_brand.predict(processed_image)
    brand_index = np.argmax(brand_prediction)  
    brand_confidence = np.max(brand_prediction)  

    size_name = size_classes[size_index] if size_confidence >= CONFIDENCE_THRESHOLD else "unknown"
    brand_name = brand_classes[brand_index] if brand_confidence >= CONFIDENCE_THRESHOLD else "unknown"

    return size_name, brand_name

def run_model(image_path, model_name): # Run the model based on the item
    model_version = 1
    model = YOLO(f"weights/{model_name}.pt")
    results = model(image_path) # Run the model on the image
    results[0].show() # Show the image with the detections
    return model, results

def check_item(item, items_model):
    print(f"Item: {item}, Model: {items_model}")
    if item == "bottle" and items_model == "GreenTech-bottle":
        return True
    if item == "can" and items_model == "GreenTech-can":
        return True
    return False

def check_detection(results):
    if len(results[0].boxes) == 0: # No detections found in the image
        return False
    return True

def check_image_format(file, image_data, filename):
    if file.content_type not in ["image/jpeg", "image/png"]: # Check if the image is in the correct format
        return False
    return True

def save_image(image_data, path_image): # Save the image on server
    print("path_image: ", path_image)
    with open(path_image, "wb") as f:
        f.write(image_data)

def move_image(image_data, cur_path, new_path): # Move the image to a new folder
    shutil.move(cur_path, new_path)
    print(f"File moved to {new_path}")

def delete_image(path_image): # Delete the image from the server
    if os.path.exists(path_image):
        os.remove(path_image)

def model_process(file, image_data, item):
    # Check if the image is in the correct format
    if not check_image_format(file, image_data, file.filename):
        raise HTTPException(status_code=400, detail={"error": "Invalid image format"})

    # Save the image on server
    path_image = f"images/{item}/valid/{file.filename}"
    print(f"Image path: {path_image}")
    save_image(image_data, path_image)


    # Run the model on the image based on the item
    model, results = run_model(path_image, "best4")
    # print(f"Results: {results}")
    # Check if the image can be classified
    if not check_detection(results):
        new_path = f"images/{item}/invalid/{file.filename}" # Invalid folder
        move_image(image_data, path_image, new_path) # Move the image to invalid folder
        raise HTTPException(status_code=400, detail={"error": "No detections found"})
    return model, results, path_image

@app.post("/processImageBottle")
async def process_image_bottle(file: UploadFile = File(...)):
    try:
        item = "bottle"

        # Read and process the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        model, results, path_image = model_process(file, image_data, item)

        # If the image is valid, classify it
        is_valid_bottle = False
        brand = "Unknown"
        size = "Unknown"
        confidence = None
        # size_confidence = None
        # brand_confidence = None
        if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
            items_model = None
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())  # Ensure this is a float
                cls = int(detection.cls.numpy())  # Ensure this is an integer
                items_model = model.names.get(cls, "Unknown")  # Safely access class name
                print(f"Class: {items_model}, Confidence: {confidence}")
            is_valid_bottle = check_item(item, items_model)
            print(f"Valid: {is_valid_bottle}")
            if not is_valid_bottle:
                valid_path = f"images/{item}/valid/{file.filename}"
                invalid_path = f"images/{item}/invalid/{file.filename}" # Invalid folder
                move_image(image_data, valid_path, invalid_path) # Move the image to invalid folder
                return {
                    "isValidBottle": is_valid_bottle,
                    "brand": brand,
                    "size": size,
                    "object_confidence": confidence
                    }

        size, brand  = predict_category(image_data, model_bottle_size, model_bottle_brand, bottle_size_classes, bottle_brand_classes)
        # model, results = run_model(path_image, "brand_model_3")
        # if check_detection(results):
        #     print("Brand detections found")
        #     if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
        #         for detection in results[0].boxes:
        #             confidence = float(detection.conf.numpy())  # Ensure this is a float
        #             cls = int(detection.cls.numpy())  # Ensure this is an integer
        #             brand = model.names.get(cls, "Unknown")  # Safely access class name
        #             print(f"Class: {brand}, Confidence: {confidence}")

        # model, results = run_model(path_image, "size_model")
        # if check_detection(results):
        #     print("Size detections found")
        #     if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
        #         for detection in results[0].boxes:
        #             confidence = float(detection.conf.numpy())  # Ensure this is a float
        #             cls = int(detection.cls.numpy())  # Ensure this is an integer
        #             size = model.names.get(cls, "Unknown")  # Safely access class name
        #             print(f"Class: {size}, Confidence: {confidence}")

        return {
            "isValidBottle": is_valid_bottle,
            "brand": brand,
            "size": size,
            "object_confidence": confidence
            # "size_confidence": size_confidence,
            # "brand_confidence": brand_confidence
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": f"Invalid image formattt: {str(e)}"})

@app.post("/processImageCan")
async def process_image_can(file: UploadFile = File(...)):
    try:
        item = "can"

        # Read and process the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        model, results, path_image = model_process(file, image_data, item)

        # If the image is valid, classify it
        brand = "Unknown"
        size = "Unknown"
        confidence = None
        if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
            is_valid_can = True
            confidence = None
            items_model = None
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())  # Ensure this is a float
                cls = int(detection.cls.numpy())  # Ensure this is an integer
                items_model = model.names.get(cls, "Unknown")  # Safely access class name
                print(f"Class: {items_model}, Confidence: {confidence}")
            is_valid_can = check_item(item, items_model)
            print(f"Valid: {is_valid_can}")
            if not is_valid_can:
                valid_path = f"images/{item}/valid/{file.filename}"
                invalid_path = f"images/{item}/invalid/{file.filename}" # Invalid folder
                move_image(image_data, valid_path, invalid_path) # Move the image to invalid folder
                return {
                    "isValidCan": is_valid_can,
                    "brand": brand,
                    "size": size,
                    "object_confidence": confidence
                    }

        size, brand = predict_category(image_data, model_can_size, model_can_brand, can_size_classes, can_brand_classes)
        # model, results = run_model(path_image, "brand_model_3")
        # if check_detection(results):
        #     print("Brand detections found")
        #     brand = "Unknown"
        #     if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
        #         for detection in results[0].boxes:
        #             confidence = float(detection.conf.numpy())  # Ensure this is a float
        #             cls = int(detection.cls.numpy())  # Ensure this is an integer
        #             brand = model.names.get(cls, "Unknown")  # Safely access class name
        #             print(f"Class: {brand}, Confidence: {confidence}")

        # model, results = run_model(path_image, "size_model")
        # if check_detection(results):
        #     print("Size detections found")
        #     size = "Unknown"
        #     if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
        #         for detection in results[0].boxes:
        #             confidence = float(detection.conf.numpy())  # Ensure this is a float
        #             cls = int(detection.cls.numpy())  # Ensure this is an integer
        #             size = model.names.get(cls, "Unknown")  # Safely access class name
        #             print(f"Class: {size}, Confidence: {confidence}")

        return {
            "isValidCan": is_valid_can,
            "brand": brand,
            "size": size,
            "object_confidence": confidence
            # "size_confidence": size_confidence,
            # "brand_confidence": brand_confidence
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": f"Invalid image formattt: {str(e)}"})

# Start the server using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# How to run if have no __main__
# uvicorn main:app --reload --port 8000
