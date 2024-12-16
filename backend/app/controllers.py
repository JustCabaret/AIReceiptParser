from modules.image_processing import preprocess_image
from modules.text_extraction import extract_text
from modules.gpt_processing import process_text_with_chatgpt
from modules.database import insert_receipt
import cv2

def process_receipt(file_path, api_key):
    """
    Receipt processing and inserts the data into the database.
    """
    # Load the image
    image = cv2.imread(file_path)

    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Extract text from the image
    extracted_text = extract_text(preprocessed_image)

    # Process the text with ChatGPT
    structured_data = process_text_with_chatgpt(extracted_text, api_key)

    # Insert the data into the database
    receipt_id = insert_receipt(structured_data)

    # Add the receipt ID to the structured data
    structured_data["receipt_id"] = receipt_id

    return structured_data