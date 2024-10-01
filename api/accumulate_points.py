from flask import Blueprint, request, jsonify
from datetime import datetime

accumulate_points_bp = Blueprint('accumulate_points', __name__)

@accumulate_points_bp.route('/accumulatePoints', methods=['POST'])
def accumulate_points():
    # data = request.json

    # phone_number = data.get('phoneNumber')
    # serial_number = data.get('serialNumber')
    # earned_points = data.get('earnedPoints')

    # # Simulate points accumulation
    # if phone_number and serial_number and earned_points:
    #     return jsonify({
    #         "depositDate": datetime.now().strftime("%d/%m/%Y"),
    #         "totalPoints": 500  # Example accumulated points
    #     }), 200
    # else:
    # return jsonify({"error": "Invalid input"}), 400
    return jsonify({
        "depositDate": datetime.now().strftime("%d/%m/%Y"),
        "totalPoints": 500  # Example accumulated points
      }), 200
