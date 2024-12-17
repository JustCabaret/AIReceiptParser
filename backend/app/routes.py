from flask import Blueprint, request, jsonify
import os
from app.controllers import process_receipt, get_all_receipts, get_receipt_details

# Define the blueprint for API routes
blueprint = Blueprint('api', __name__)

@blueprint.route('/process_receipt', methods=['POST'])
def process_receipt_route():
    """
    Endpoint to process a receipt image.
    """
    try:
        # Validate if 'file' is present in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        api_key = request.form.get('api_key')

        # Validate input
        if not api_key:
            return jsonify({"error": "Missing API key"}), 400
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save the file temporarily
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)

        # Process the file
        result = process_receipt(file_path, api_key)

        # Clean up the temporary file
        os.remove(file_path)

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        # Return errors in JSON format
        return jsonify({"error": str(e)}), 500

@blueprint.route('/receipts', methods=['GET'])
def get_all_receipts_route():
    """
    Endpoint to retrieve all receipts with main details.
    Returns:
    - JSON containing a list of receipts with 'id', 'total', and 'store'.
    """
    try:
        receipts = get_all_receipts()
        return jsonify(receipts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint.route('/receipts/<int:receipt_id>', methods=['GET'])
def get_receipt_details_route(receipt_id):
    """
    Endpoint to retrieve details of a specific receipt.
    Returns:
    - JSON containing the products of the receipt.
    """
    try:
        details = get_receipt_details(receipt_id)
        return jsonify(details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
