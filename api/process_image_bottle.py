from flask import Blueprint, request, jsonify

process_image_bottle_bp = Blueprint('process_image_bottle', __name__)

@process_image_bottle_bp.route('/processImageBottle', methods=['POST'])

def process_image_bottle():
    # if 'imageFile' not in request.files:
    #     return jsonify({"error": "Invalid image file"}), 400

    # Simulate image processing
    return jsonify({
        "isValidBottle": True,
        "brand": "oishi",
        "size": 500,
        "confidence": 0.89
    }), 200

