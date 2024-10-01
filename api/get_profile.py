from flask import Blueprint, request, jsonify
# import requests

get_profile_bp = Blueprint('get_profile', __name__)

# Configure your Strapi API endpoint and API token here
STRAPI_API_URL = "http://localhost:1337/api/users"
STRAPI_API_TOKEN = "your_strapi_api_token_here"  # Optional if authentication is required

@get_profile_bp.route('/getProfile', methods=['POST'])
def get_profile():
    # data = request.json
    # phone_number = data.get('phoneNumber')

    # if not phone_number:
    #     return jsonify({"error": "Phone number is required"}), 400

    # try:
    #     # Make a request to the Strapi API to fetch the user data based on the phone number
    #     headers = {
    #         "Authorization": f"Bearer {STRAPI_API_TOKEN}",
    #         "Content-Type": "application/json"
    #     }

    #     # Assuming the phone number is a field in your Strapi user collection
    #     response = requests.get(f"{STRAPI_API_URL}?filters[phoneNumber][$eq]={phone_number}", headers=headers)

    #     # Check if the response is successful
    #     if response.status_code == 200:
    #         user_data = response.json()

    #         if user_data and user_data['data']:
    #             # Assuming Strapi response contains the fields `username`, `fullName`, and `totalPoint`
    #             user = user_data['data'][0]
    #             return jsonify({
    #                 "username": user['username'],
    #                 "fullName": user['fullName'],
    #                 "totalPoint": user['totalPoint']
    #             }), 200
    #         else:
    #             return jsonify({"error": "User not found"}), 404

    #     # If Strapi API fails
    #     return jsonify({"error": "Failed to fetch data from Strapi"}), 500

    # except requests.exceptions.RequestException as e:
    #     # Catch any errors during the HTTP request
    #     return jsonify({"error": "Internal server error", "details": str(e)}), 500
    return jsonify({
              "username": "Mobile",
              "fullName": "Phatcharamon",
              "totalPoint": 250
          }), 200
