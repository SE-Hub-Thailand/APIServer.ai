from flask import Blueprint, request, jsonify
import requests

# Blueprint for the API
calculate_can_points_bp = Blueprint('calculate_can_points', __name__)

# Strapi API configuration
API_URL = "https://cookbstaging.careervio.com"
STRAPI_API_URL = f"{API_URL}/api/formulas"
# STRAPI_API_URL = "http://209.58.160.245:1337/api/users"
STRAPI_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaWF0IjoxNzI3NTMwMjk5LCJleHAiOjE3MzAxMjIyOTl9.tHMG9oYjv8Rp_qwp_uikyrcuwEBRZLjQauUu1p_s5QY"  # Optional if authentication is required

# Fetch formula data from Strapi
def fetch_can_formula_data():
    headers = {
        "Authorization": f"Bearer {STRAPI_API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{STRAPI_API_URL}", headers=headers)
        if response.status_code == 200:
            return response.json()['data']  # Return data from Strapi
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching can formula data: {e}")
        return None

# Function to calculate earned points
@calculate_can_points_bp.route('/calculatedCanPoints', methods=['POST'])
def calculate_can_points():
    data = request.json  # Get the JSON data from the request body

    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input"}), 400

    # Fetch formula data from Strapi
    formula_data = fetch_can_formula_data()

    if not formula_data:
        return jsonify({"error": "Internal server error"}), 500

    print("Formula data:", formula_data)
    # print("formula['attributes']['size']", formula['attributes']['size'])
    # Create a dictionary mapping can size to points
    size_point_mapping = {
        formula['attributes']['size']: formula['attributes']['point'] for formula in formula_data
    }

    total_cans = 0
    earned_points = 0

    # Calculate total cans and earned points based on input data and formula from Strapi
    for item in data:
        can_size = item.get('canSize')
        quantity = item.get('quantity')

        if not can_size or not isinstance(quantity, int):
            return jsonify({"error": "Invalid input"}), 400

        # Get points for the given can size, default to 0 if size not found
        points_per_can = size_point_mapping.get(can_size, 0)
        total_cans += quantity

        if points_per_can:
            earned_points += points_per_can * quantity
        # else:
        #     return jsonify({"error": f"Can size '{can_size}' not found"}), 400

    return jsonify({
        "earnedPoints": earned_points,
        "totalCans": total_cans
    }), 200

    # return jsonify({
    #     "earnedPoints": 150,
    #     "totalCans": 3
    # }), 200
