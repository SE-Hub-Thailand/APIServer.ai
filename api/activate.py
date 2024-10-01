from flask import Blueprint, request, jsonify
import requests

# Define the blueprint for the activate API
activate_bp = Blueprint('activate', __name__)

# Configure your Strapi API endpoint and API token (if needed)
STRAPI_API_URL = "http://localhost:1337/api/machines"  # Replace with your actual Strapi endpoint
STRAPI_API_TOKEN = "your_strapi_api_token"  # Use if your Strapi API requires authentication

@activate_bp.route('/activate', methods=['POST'])
def activate():
    """
    API endpoint to activate a machine. It checks whether the serial number is a duplicate.
    """
    # data = request.json
    # serial_number = data.get('serialNumber')

    # if not serial_number:
    #     return jsonify({"error": "Invalid input"}), 400

    # # Check for duplicate serial numbers by fetching data from Strapi
    # try:
    #     # Set up the headers for the request (if Strapi API token is required)
    #     headers = {
    #         "Authorization": f"Bearer {STRAPI_API_TOKEN}",
    #         "Content-Type": "application/json"
    #     }

    #     # Send a GET request to Strapi to retrieve the list of machines and their serial numbers
    #     response = requests.get(STRAPI_API_URL, headers=headers)

    #     # Check if the request was successful
    #     if response.status_code == 200:
    #         machines = response.json()['data']

    #         # Check if the provided serial number already exists
    #         for machine in machines:
    #             if machine['attributes']['serialNumber'] == serial_number:
    #                 # If a duplicate is found, return an error response
    #                 return jsonify({"error": "Duplicate serial number"}), 400

    #         # If no duplicate is found, proceed with the activation
    #         # You would typically save the new machine record here (not shown in this example)
    #         return jsonify({
    #             "serialNumber": serial_number,
    #             "status": "activated"
    #         }), 200

    #     else:
    #         # If the Strapi request fails, return an error
    #         return jsonify({"error": "Failed to fetch data from Strapi"}), 500

    # except requests.exceptions.RequestException as e:
    #     # Catch any errors during the HTTP request
    #     return jsonify({"error": "Internal server error", "details": str(e)}), 500

    return jsonify({
        "serialNumber": "1234567890",
        "status": "activated"
    }), 200
