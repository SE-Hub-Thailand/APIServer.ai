import requests
from flask import Blueprint, request, jsonify
from datetime import datetime

accumulate_points_bp = Blueprint('accumulate_points', __name__)

# Assuming your Strapi API is running on localhost at port 1337
API_URL = "http://209.58.160.245:1337"
STRAPI_API_URL = f"{API_URL}/api/history-machine"
STRAPI_API_URL_USER = f"{API_URL}/api/users"
STRAPI_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaWF0IjoxNzI3NTMwMjk5LCJleHAiOjE3MzAxMjIyOTl9.tHMG9oYjv8Rp_qwp_uikyrcuwEBRZLjQauUu1p_s5QY"  # Optional if authentication is required


@accumulate_points_bp.route('/accumulatePoints', methods=['POST'])
def accumulate_points():
    data = request.json

    phone_number = data.get('telNumber')
    serial_number = data.get('serialNumber')
    earned_points = data.get('earnedPoints')

    if phone_number and serial_number and earned_points:
        response = requests.get(f"{STRAPI_API_URL}?filters[telNumber][$eq]={phone_number}", headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            user_data = response.json()

            if user_data and user_data[0]:
                # Assuming Strapi response contains the fields `username`, `fullName`, and `point`
                user = user_data[0]
                return jsonify({
                    "username": user['username'],
                    "fullName": user['fullName'],
                    "point": user['point']
                }), 200
            else:
                return jsonify({"error": "User not found"}), 404
        # Prepare data to send to Strapi
        strapi_data = {
            "data": {
                "phoneNumber": phone_number,
                "serialNumber": serial_number,
                "point": earned_points,
                "date": datetime.now().isoformat(),
                "time": datetime.now().strftime("%H:%M"),

            }
        }

        # Set up headers for the request
        headers = {
            "Authorization": f"Bearer {STRAPI_API_TOKEN}",
            "Content-Type": "application/json"
        }

        try:
            # Send a POST request to Strapi to create a new entry
            response = requests.post(STRAPI_API_URL, json=strapi_data, headers=headers)

            if response.status_code == 200 or response.status_code == 201:
                return jsonify({
                    "message": "Points accumulated successfully",
                    "point": earned_points
                }), 200
            else:
                return jsonify({"error": "Failed to accumulate points in Strapi"}), response.status_code
        except requests.RequestException as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid input"}), 400

    # return jsonify({
    #     "depositDate": datetime.now().strftime("%d/%m/%Y"),
    #     "totalPoints": 500  # Example accumulated points
    #   }), 200
