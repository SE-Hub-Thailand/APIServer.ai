from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics import YOLO
from PIL import Image
import io
import os
import shutil

app = FastAPI()

def run_model(image_path): # Run the model based on the item
    model_version = 1
    model = YOLO(f"weights/best{model_version}.pt")
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
    model, results = run_model(path_image)
    print(f"Results: {results}")
    # Check if the image can be classified
    if not check_detection(results):
        new_path = f"images/{item}/invalid/{file.filename}" # Invalid folder
        move_image(image_data, path_image, new_path) # Move the image to invalid folder
        raise HTTPException(status_code=400, detail={"error": "No detections found"})
    return model, results

@app.post("/processImageBottle")
async def process_image_bottle(file: UploadFile = File(...)):
    try:
        item = "bottle"

        # Read and process the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        model, results = model_process(file, image_data, item)

        # If the image is valid, classify it
        if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
            is_valid_bottle = True
            confidence = None
            items_model = None
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())  # Ensure this is a float
                cls = int(detection.cls.numpy())  # Ensure this is an integer
                items_model = model.names.get(cls, "Unknown")  # Safely access class name
                print(f"Class: {items_model}, Confidence: {confidence}")
            is_valid_bottle = check_item(item, items_model)
            if not is_valid_bottle:
                valid_path = f"images/{item}/valid/{file.filename}"
                invalid_path = f"images/{item}/invalid/{file.filename}" # Invalid folder
                move_image(image_data, valid_path, invalid_path) # Move the image to invalid folder
            return {
                "isValidBottle": is_valid_bottle,
                "confidence": confidence
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

        model, results = model_process(file, image_data, item)

        # If the image is valid, classify it
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
                "confidence": confidence
                }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": f"Invalid image formattt: {str(e)}"})

# Start the server using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# How to run if have no __main__
# uvicorn main:app --reload --port 8000
