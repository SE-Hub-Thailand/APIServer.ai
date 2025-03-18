#!/bin/bash

# สร้าง Virtual Environment
python3 -m venv venv
# python3.11 -m venv venv # for use tensorflow

# เปิดใช้งาน Virtual Environment
source ./venv/bin/activate

# ติดตั้ง dependencies ที่จำเป็น
pip install uvicorn
pip install fastapi
pip install python-multipart
pip install ultralytics
pip install Flask
pip install Pillow
pip install numpy
pip install tensorflow

# อัปเดตระบบและติดตั้ง libgl1 สำหรับ OpenCV
sudo apt update
sudo apt install -y libgl1

echo "Setup completed successfully."
