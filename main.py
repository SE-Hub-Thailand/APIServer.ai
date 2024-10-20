from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics import YOLO
from PIL import Image
import io
import os
import shutil
import requests
# import numpy as numpy

app = FastAPI()
API_URL = "https://cookbstaging.careervio.com"
# "http://64.227.31.13:1337"

def upload_image_to_strapi(image_data, filename):
    url = f"{API_URL}/api/upload"  # เปลี่ยน URL นี้เป็น URL ของ Strapi

    files = {
        'files': (filename, image_data, 'image/jpeg')
    }

    response = requests.post(url, files=files)

    if response.status_code == 200:
        print(f"Uploaded {filename} to Strapi successfully.")
        return response.json()
    else:
        print(f"Failed to upload {filename} to Strapi: {response.status_code}, {response.text}")
        raise HTTPException(status_code=500, detail="Failed to upload image to Strapi")

# def save_image(image_data, path_image):
#     os.makedirs(os.path.dirname(path_image), exist_ok=True)
#     with open(path_image, "wb") as f:
#         f.write(image_data)

# def delete_image(path_image):
#     if os.path.exists(path_image):
#         os.remove(path_image)

# def move_image(cur_path, new_path):
#     os.makedirs(os.path.dirname(new_path), exist_ok=True)
#     shutil.move(cur_path, new_path)

def run_model(image_path, model_name):
    model = YOLO(f"weights/{model_name}.pt")
    results = model(image_path)
    return model, results

def check_item(item, items_model):
    if item == "bottle" and items_model == "GreenTech-bottle":
        return True
    if item == "can" and items_model == "GreenTech-can":
        return True
    return False

def check_detection(results):
    if len(results[0].boxes) == 0:
        return False
    return True

def check_image_format(file):
    if file.content_type not in ["image/jpeg", "image/png"]:
        return False
    return True

def model_process(file, image_data, item):
    if not check_image_format(file):
        raise HTTPException(status_code=400, detail={"error": "Invalid image format"})

    # อัปโหลดรูปภาพไปยัง Strapi
    upload_response = upload_image_to_strapi(image_data, file.filename)

    # ดึง URL ของรูปภาพที่อัปโหลดมาจากการตอบสนองของ Strapi
    image_url = f"{API_URL}{upload_response[0]['url']}"  # การเข้าถึงข้อมูลอาจแตกต่างกันขึ้นอยู่กับโครงสร้างของการตอบสนองจาก Strapi
    print(f"Image URL: {image_url}")

    # รันโมเดลโดยใช้ URL ของรูปภาพ
    model, results = run_model(image_url, "best4")
    if not check_detection(results):
        raise HTTPException(status_code=400, detail={"error": "No detections found"})

    return model, results, image_url

@app.post("/processImageBottle")
async def process_image_bottle(file: UploadFile = File(...)):
    try:
        item = "bottle"
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        model, results, path_image = model_process(file, image_data, item)

        is_valid_bottle = False
        brand = "Unknown"
        size = "Unknown"
        confidence = None

        if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
            items_model = None
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())
                cls = int(detection.cls.numpy())
                items_model = model.names.get(cls, "Unknown")
            is_valid_bottle = check_item(item, items_model)

            if not is_valid_bottle:
                # invalid_path = f"images/{item}/invalid/{file.filename}"
                # move_image(path_image, invalid_path)
                return {"isValidBottle": is_valid_bottle, "brand": brand, "size": size, "confidence": confidence}

        model, results = run_model(path_image, "brand_model_3")
        if check_detection(results):
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())
                cls = int(detection.cls.numpy())
                brand = model.names.get(cls, "Unknown")

        model, results = run_model(path_image, "size_model")
        if check_detection(results):
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())
                cls = int(detection.cls.numpy())
                size = model.names.get(cls, "Unknown")

        return {"isValidBottle": is_valid_bottle, "brand": brand, "size": size, "confidence": confidence}
    except Exception as e:
        raise HTTPException(detail={"error": f"Invalid image format: {str(e)}"})

@app.post("/processImageCan")
async def process_image_can(file: UploadFile = File(...)):
    try:
        item = "can"
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        model, results, path_image = model_process(file, image_data, item)

        brand = "Unknown"
        size = "Unknown"
        confidence = None

        if len(results[0].boxes) > 0 and hasattr(results[0], 'boxes'):
            is_valid_can = True
            items_model = None
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())
                cls = int(detection.cls.numpy())
                items_model = model.names.get(cls, "Unknown")
            is_valid_can = check_item(item, items_model)

            if not is_valid_can:
                # invalid_path = f"images/{item}/invalid/{file.filename}"
                # move_image(path_image, invalid_path)
                return {"isValidCan": is_valid_can, "brand": brand, "size": size, "confidence": confidence}

        model, results = run_model(path_image, "brand_model_3")
        if check_detection(results):
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())
                cls = int(detection.cls.numpy())
                brand = model.names.get(cls, "Unknown")

        model, results = run_model(path_image, "size_model")
        if check_detection(results):
            for detection in results[0].boxes:
                confidence = float(detection.conf.numpy())
                cls = int(detection.cls.numpy())
                size = model.names.get(cls, "Unknown")

        return {"isValidCan": is_valid_can, "brand": brand, "size": size, "confidence": confidence}
    except Exception as e:
        raise HTTPException(detail={"error": f"Invalid image format: {str(e)}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# How to run the server
## uvicorn main:app --reload --port 8000
