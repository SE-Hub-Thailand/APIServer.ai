from flask import Blueprint, request, jsonify
import requests
import logging

heartbeat_bp = Blueprint('heartbeat', __name__)

@heartbeat_bp.route('/heartbeat', methods=['POST'])

def heartbeat():
    data = request.json
    serial_number = data.get('serialNumber')

    if serial_number:
        return jsonify({
            "serialNumber": serial_number,
            "status": "online"
        }), 200
    else:
        return jsonify({"error": "RVM not found"}), 404
    # return jsonify({
    #         "serialNumber": "1234567890",
    #         "status": "online"
    #     }), 200

# # Setup logging to keep track of machine status checks
# logging.basicConfig(filename='/path/to/your/logfile.log', level=logging.INFO)

# # Configure your machine's serial number and API endpoint
# SERIAL_NUMBER = 'RVM123456'
# HEARTBEAT_URL = 'http://localhost:5000/heartbeat'  # Replace with the actual endpoint URL

# def check_machine_status():
#     try:
#         response = requests.post(HEARTBEAT_URL, json={"serialNumber": SERIAL_NUMBER})
#         if response.status_code == 200:
#             status_data = response.json()
#             logging.info(f"Machine {SERIAL_NUMBER} status: {status_data['status']}")
#         else:
#             logging.error(f"Error: Received status code {response.status_code}")
#     except Exception as e:
#         logging.error(f"Failed to check machine status: {str(e)}")

# if __name__ == "__main__":
#     check_machine_status()
