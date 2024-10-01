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
