from flask import Blueprint, request, jsonify
import requests  # Uncommented since you need this for making HTTP requests

get_profile_bp = Blueprint('get_profile', __name__)

# Configure your Strapi API endpoint and API token here
# API_URL = "https://cookbstaging.careervio.com"
# STRAPI_API_URL = f"{API_URL}/api/users"
STRAPI_API_URL = "http://209.58.160.245:1337/api/users"
STRAPI_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaWF0IjoxNzI3NTMwMjk5LCJleHAiOjE3MzAxMjIyOTl9.tHMG9oYjv8Rp_qwp_uikyrcuwEBRZLjQauUu1p_s5QY"  # Optional if authentication is required

@get_profile_bp.route('/getProfile', methods=['POST'])
def get_profile():
    data = request.json
    telNumber = data.get('telNumber')
    print("telNumber: ", telNumber)
    print("data: ", data)
    if not telNumber:
        return jsonify({"error": "Phone number is required"}), 400

    try:
        # Make a request to the Strapi API to fetch the user data based on the phone number
        headers = {
            "Authorization": f"Bearer {STRAPI_API_TOKEN}",
            "Content-Type": "application/json"
        }

        # Assuming the phone number is a field in your Strapi user collection
        response = requests.get(f"{STRAPI_API_URL}?filters[telNumber][$eq]={telNumber}", headers=headers)

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

        # If Strapi API fails
        return jsonify({"error": "Failed to fetch data from Strapi"}), 500

    except requests.exceptions.RequestException as e:
        # Catch any errors during the HTTP request
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

