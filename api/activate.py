from flask import Blueprint, request, jsonify
import requests

# Define the blueprint for the activate API
activate_bp = Blueprint('activate', __name__)

# Configure your Strapi API endpoint and API token (if needed)
# API_URL = "https://cookbstaging.careervio.com"
API_URL = "http://209.58.160.245:1337"
STRAPI_API_URL = f"{API_URL}/api/recycle-machines"
STRAPI_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaWF0IjoxNzI3NTMwMjk5LCJleHAiOjE3MzAxMjIyOTl9.tHMG9oYjv8Rp_qwp_uikyrcuwEBRZLjQauUu1p_s5QY"  # Optional if authentication is required


@activate_bp.route('/activate', methods=['POST'])
def activate():
    """
    API endpoint to activate a machine. It checks whether the serial number is valid and activates the machine.
    """
    # Get the serialNumber from the request body
    data = request.json
    serial_number = data.get('serialNumber')
    print("Hello: ", serial_number)
    if not serial_number:
        return jsonify({"error": "Invalid input, serial number is required"}), 400

    # Check for the serial number in Strapi
    try:
        # Set up the headers for the request (if Strapi API token is required)
        headers = {
            "Authorization": f"Bearer {STRAPI_API_TOKEN}",
            "Content-Type": "application/json"
        }
        print("Hello2")
        # Send a GET request to Strapi to find the machine with the given serial number
        response = requests.get(f"{STRAPI_API_URL}?filters[serialNumber][$eq]={serial_number}", headers=headers)
        print("response:", response)
        # Check if the request was successful
        if response.status_code == 200:
            machines = response.json().get('data', [])

            # If no machine is found with the provided serial number
            # if not machines:
            #     return jsonify({"error": "Machine not found"}), 404

            # Get the first machine found (assuming serial numbers are unique)
            # machine = machines[0]
            print("Machine:", machines)
            machine = machines[0]
            print("Machine:", machine)
            # print("Machine:", machine['data']['attributes'])
            # print("Machine:", machine['data']['attributes'][0])
            activated = machine['attributes'].get('activated')

            # Check if the machine is already activated
            if activated:
                return jsonify({"error": "The machine has already been activated. Duplicate activation is not allowed."}), 400

            # If not activated, update the machine's activated status to true
            machine_id = machine['id']
            print("Machine ID:", machine_id)
            update_data = {
                "data": {
                    # "location": "string",
                    # "latitude": "string",
                    # "longitude": "string",
                    # "serialNumber": "string",
                    "activated": True
                    # "ownerName": "string"
                }
            }

            # Send a PUT request to Strapi to update the machine's status
            update_response = requests.put(f"{STRAPI_API_URL}/{machine_id}", json=update_data, headers=headers)

            if update_response.status_code in [200, 204]:
                return jsonify({
                    "serialNumber": serial_number,
                    "status": "The machine is activated now"
                }), 200
            else:
                return jsonify({"error": "Failed to update the machine status"}), 500

        else:
            # If the Strapi request fails, return an error
            return jsonify({"error": "Failed to fetch data from Strapi"}), 500

    except requests.exceptions.RequestException as e:
        # Catch any errors during the HTTP request
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
