from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Sample data for users
users = [
    {
        "phoneNumber": "0000000000",
        "username": "Mobile",
        "fullName": "Phatcharamon Namwayko",
        "totalPoint": 350
    }
]

# Sample point system
bottle_points = {"325 ml": 50, "500 ml": 100}
can_points = {"325 ml": 50, "500 ml": 100}

# Models for input validation
class PhoneNumberRequest(BaseModel):
    phoneNumber: str

class BottleDeposit(BaseModel):
    bottleSize: str
    quantity: int

class CanDeposit(BaseModel):
    canSize: str
    quantity: int

class AccumulatePointsRequest(BaseModel):
    phoneNumber: str
    serialNumber: str
    earnedPoints: int

class DonateRequest(BaseModel):
    phoneNumber: str

class ActivateRequest(BaseModel):
    serialNumber: str

class HeartbeatRequest(BaseModel):
    serialNumber: str

# 1. POST /getProfile
@app.post("/getProfile")
async def get_profile(request: PhoneNumberRequest):
    # phone_number = request.phoneNumber
    # phone_number = '0000000000'
    # user = next((u for u in users if u['phoneNumber'] == phone_number), None)

    # if user:
    #     return {
    #         "username": user['username'],
    #         "fullName": user['fullName'],
    #         "totalPoint": user['totalPoint']
    #     }
    # else:
    #     raise HTTPException(status_code=404, detail="User not found")
    return {
            "username": "username",
            "fullName": "fullName",
            "totalPoint": "totalPoint"
        }

# 2. POST /calculatedBottlePoints
@app.post("/calculatedBottlePoints")
async def calculate_bottle_points(jsonObj: list[BottleDeposit]):
    total_points = 0
    total_bottles = 0

    # for item in jsonObj:
    #     if item.bottleSize not in bottle_points:
    #         raise HTTPException(status_code=400, detail="Invalid bottle size")

    #     total_points += bottle_points[item.bottleSize] * item.quantity
    #     total_bottles += item.quantity

    return {
        "earnedPoints": total_points,
        "totalBottles": total_bottles
    }

# 3. POST /calculatedCanPoints
@app.post("/calculatedCanPoints")
async def calculate_can_points(jsonObj: list[CanDeposit]):
    total_points = 0
    total_cans = 0

    # for item in jsonObj:
    #     if item.canSize not in can_points:
    #         raise HTTPException(status_code=400, detail="Invalid can size")

    #     total_points += can_points[item.canSize] * item.quantity
    #     total_cans += item.quantity

    return {
        "earnedPoints": total_points,
        "totalCans": total_cans
    }

# 4. POST /accumulatePoints
@app.post("/accumulatePoints")
async def accumulate_points(request: AccumulatePointsRequest):
    # phone_number = request.phoneNumber
    # user = next((u for u in users if u['phoneNumber'] == phone_number), None)

    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    # # Add earned points to the user's total points
    # user['totalPoint'] += request.earnedPoints

    # return {
    #     "depositDate": datetime.now().strftime("%d/%m/%Y"),
    #     "totalPoints": user['totalPoint']
    # }
        return {
        "depositDate": datetime.now().strftime("%d/%m/%Y"),
        "totalPoints": "totalPoint"
    }

# 5. POST /donate
@app.post("/donate")
async def donate(data: DonateRequest):
    phone_number = data.phoneNumber

    # ตรวจสอบความถูกต้องของหมายเลขโทรศัพท์ (ตัวอย่างเช่น ตรวจสอบรูปแบบ)
    # if len(phone_number) != 10 or not phone_number.isdigit():
    #     raise HTTPException(status_code=400, detail="Invalid phone number")

    # try:
        # บันทึกข้อมูลการบริจาคไปยังฐานข้อมูล (เช่น Strapi)
        # ตัวอย่างการบันทึกข้อมูล
        # save_donation(phone_number)

    return {"message": "Donation data saved successfully"}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Internal server error")

# 6. POST /activate
async def activate(data: ActivateRequest):
    serial_number = data.serialNumber

    # try:
        # ตรวจสอบสถานะของเครื่อง RVM (เช่น ดูจากฐานข้อมูล)
        # rvm_status = check_rvm_status(serial_number)

        # ตัวอย่าง: ถ้าเครื่องถูก Activate แล้ว
        # rvm_status = "activated"  # สมมุติว่าเป็นค่าเบื้องต้น

        # if rvm_status == "activated":
    return {"serialNumber": serial_number, "status": "activated"}
    #     else:
    #         raise HTTPException(status_code=404, detail="RVM not found")

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Internal server error")

# 7. POST /heartbeat
@app.post("/heartbeat")
async def heartbeat(data: HeartbeatRequest):
    serial_number = data.serialNumber

    # try:
        # ตรวจสอบสถานะออนไลน์ของเครื่อง RVM (เช่น ดูจากฐานข้อมูล)
        # rvm_status = check_rvm_online_status(serial_number)

        # ตัวอย่าง: ถ้าเครื่องออนไลน์
        # rvm_status = "online"  # สมมุติว่าเป็นค่าเบื้องต้น

        # if rvm_status == "online":
    return {"serialNumber": serial_number, "status": "online"}
    #     else:
    #         raise HTTPException(status_code=404, detail="RVM not found")

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Internal server error")

# Error handling for unexpected server issues
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    return {"error": "Internal server error"}


# Start the server using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
