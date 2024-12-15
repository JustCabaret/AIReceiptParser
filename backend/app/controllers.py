from modules.image_processing import preprocess_image
from modules.text_extraction import extract_text
from modules.gpt_processing import process_text_with_chatgpt
import cv2

def process_receipt(file_path, api_key):
    """
    Orchestrates receipt processing:
    1. Loads the uploaded image.
    2. Preprocesses the image.
    3. Extracts text using OCR.
    4. Processes text with ChatGPT.
    """
    # Load the image
    image = cv2.imread(file_path)

    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Extract text from the image
    extracted_text = extract_text(preprocessed_image)

    # Process the text with ChatGPT
    structured_data = process_text_with_chatgpt(extracted_text, api_key)

    return structured_data