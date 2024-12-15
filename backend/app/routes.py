from flask import Blueprint, request, jsonify
import os
from app.controllers import process_receipt

blueprint = Blueprint('api', __name__)

@blueprint.route('/process_receipt', methods=['POST'])
def process_receipt_route():
    """
    Endpoint to process a receipt image.
    Accepts:
    - Multipart/form-data with 'file' (image) and 'api_key' (OpenAI API key).
    """
    try:
        # Check if the 'file' part exists in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        api_key = request.form.get('api_key')

        # Validate the input
        if not api_key:
            return jsonify({"error": "Missing API key"}), 400
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save the uploaded file temporarily
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)

        # Process the file
        result = process_receipt(file_path, api_key)

        # Clean up the temporary file
        os.remove(file_path)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500