import pytesseract

def extract_text(image):
    """
    Extracts text from a preprocessed image using Tesseract OCR.
    """
    return pytesseract.image_to_string(image)