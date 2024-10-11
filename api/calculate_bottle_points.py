from flask import Blueprint, request, jsonify
import requests

# Blueprint for the API
calculate_bottle_points_bp = Blueprint('calculate_bottle_points', __name__)

# Strapi API configuration
API_URL = "https://cookbstaging.careervio.com"
STRAPI_API_URL = f"{API_URL}/api/formulas"
STRAPI_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaWF0IjoxNzI3NTMwMjk5LCJleHAiOjE3MzAxMjIyOTl9.tHMG9oYjv8Rp_qwp_uikyrcuwEBRZLjQauUu1p_s5QY"  # Replace with your Strapi API token

# Fetch formula data from Strapi for bottles
def fetch_bottle_formula_data():
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
        print(f"Error fetching bottle formula data: {e}")
        return None

# Function to calculate earned points for bottles
@calculate_bottle_points_bp.route('/calculatedBottlePoints', methods=['POST'])
def calculate_bottle_points():
    data = request.json  # Get the JSON data from the request body

    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input"}), 400

    # Fetch formula data for bottles from Strapi
    formula_data = fetch_bottle_formula_data()

    if not formula_data:
        return jsonify({"error": "Internal server error"}), 500

    # Create a dictionary mapping bottle size to points
    size_point_mapping = {
        formula['attributes']['size']: formula['attributes']['point'] for formula in formula_data
    }

    total_bottles = 0
    earned_points = 0

    # Calculate total bottles and earned points based on input data and formula from Strapi
    for item in data:
        bottle_size = item.get('bottleSize')
        quantity = item.get('quantity')

        if not bottle_size or not isinstance(quantity, int):
            return jsonify({"error": "Invalid input"}), 400

        # Get points for the given bottle size, default to 0 if size not found
        points_per_bottle = size_point_mapping.get(bottle_size, 0)
        total_bottles += quantity
        
        if points_per_bottle:
            earned_points += points_per_bottle * quantity

    return jsonify({
        "earnedPoints": earned_points,
        "totalBottles": total_bottles
    }), 200
