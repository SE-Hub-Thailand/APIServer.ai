from flask import Blueprint, request, jsonify

donate_bp = Blueprint('donate', __name__)

@donate_bp.route('/donate', methods=['POST'])
def donate():
    # data = request.json
    # phone_number = data.get('phoneNumber')

    # # Simulate donation saving
    # if phone_number:
    #     return jsonify({"message": "Donation data saved successfully"}), 200
    # else:
    #     return jsonify({"error": "Invalid phone number"}), 400
    return jsonify({"message": "Donation data saved successfully"}), 200
