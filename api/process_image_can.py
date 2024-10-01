from flask import Blueprint, request, jsonify

process_image_can_bp = Blueprint('process_image_can', __name__)

@process_image_can_bp.route('/processImageCan', methods=['POST'])

def process_image_can():
    # if 'imageFile' not in request.files:
    #     return jsonify({"error": "Invalid image file"}), 400

    # Simulate image processing
    return jsonify({
        "isValidCan": True,
        "brand": "pepsi",
        "size": 325,
        "confidence": 0.98
    }), 200

