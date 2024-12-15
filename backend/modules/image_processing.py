import cv2

def preprocess_image(image):
    """
    Preprocesses the image:
    1. Converts to grayscale.
    2. Applies thresholding for better contrast.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return threshold
