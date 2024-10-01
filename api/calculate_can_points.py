from flask import Blueprint, request, jsonify

calculate_can_points_bp = Blueprint('calculate_can_points', __name__)

@calculate_can_points_bp.route('/calculatedCanPoints', methods=['POST'])
def calculate_can_points():
    # data = request.json

    # # Simulate points calculation
    # total_cans = sum(item['quantity'] for item in data)
    # earned_points = total_cans * 50  # Example point logic

    # return jsonify({
    #     "earnedPoints": earned_points,
    #     "totalCans": total_cans
    # }), 200
    return jsonify({
        "earnedPoints": 150,
        "totalCans": 3
    }), 200
