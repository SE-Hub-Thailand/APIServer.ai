from flask import Blueprint, request, jsonify

calculate_bottle_points_bp = Blueprint('calculate_bottle_points', __name__)

@calculate_bottle_points_bp.route('/calculatedBottlePoints', methods=['POST'])
def calculate_bottle_points():
    # data = request.json

    # # Simulate points calculation
    # total_bottles = sum(item['quantity'] for item in data)
    # earned_points = total_bottles * 50  # Example point logic

    # return jsonify({
    #     "earnedPoints": earned_points,
    #     "totalBottles": total_bottles
    # }), 200
	return jsonify({
        "earnedPoints": 300,
        "totalBottles": 5
    }), 200
