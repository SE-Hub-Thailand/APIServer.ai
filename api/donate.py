from flask import Blueprint, request, jsonify
import requests
from datetime import datetime

donate_bp = Blueprint('donate', __name__)

# Strapi API configuration
# API_URL = "https://cookbstaging.careervio.com"
API_URL = "http://209.58.160.245:1337"

STRAPI_API_URL_DONATE = f"{API_URL}/api/donates"  # Endpoint สำหรับสร้าง record การบริจาค
STRAPI_API_URL_USERS = f"{API_URL}/api/users"  # Endpoint สำหรับค้นหา user
STRAPI_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaWF0IjoxNzI3NTMwMjk5LCJleHAiOjE3MzAxMjIyOTl9.tHMG9oYjv8Rp_qwp_uikyrcuwEBRZLjQauUu1p_s5QY"  # Replace with your actual Strapi API token

# Function to create a new donation in Strapi
@donate_bp.route('/donate', methods=['POST'])
def donate():
    data = request.json
    telNumber = data.get('telNumber')
    donate_point = data.get('donatePoint')  # Assuming point are passed in the request

    if not telNumber or not donate_point:
        return jsonify({"error": "Phone number and donate point are required"}), 400

    # Get the current date and time for the donation
    current_date = datetime.now().isoformat()

    # Fetch the user from Strapi based on the phone number (telNumber)
    headers = {
        "Authorization": f"Bearer {STRAPI_API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Search for the user by phone number
        user_response = requests.get(f"{STRAPI_API_URL_USERS}?filters[telNumber][$eq]={telNumber}", headers=headers)
        # response = requests.get(f"{STRAPI_API_URL}?filters[telNumber][$eq]={telNumber}", headers=headers)

        if user_response.status_code != 200:
            return jsonify({"error": "Failed to fetch user from Strapi"}), 500

        users = user_response.json()
        if not users:
            return jsonify({"error": "User not found"}), 404

        # Assuming the first user match is the correct user
        user_id = users[0]['id']

        # Prepare the donation data to send to Strapi
        donation_data = {
            "data": {
                "date": current_date,
                "donatePoint": donate_point,
                "user": user_id  # Associate donation with the user
            }
        }

        # Send the POST request to Strapi to create a new donation record
        donation_response = requests.post(STRAPI_API_URL_DONATE, json=donation_data, headers=headers)

        # Check if the donation was created successfully
        if donation_response.status_code == 200 or donation_response.status_code == 201:
            return jsonify({"message": "Donation data saved successfully"}), 200
        else:
            error_response = donation_response.json()
            return jsonify({"error": "Failed to save donation data", "details": error_response}), 500

    except requests.exceptions.RequestException as e:
        # Handle errors that occur during the HTTP request
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
