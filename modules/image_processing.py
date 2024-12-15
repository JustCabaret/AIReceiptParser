import cv2

def preprocess_image(image_path):
    image = cv2.imread(image_path)

    # Convertendo para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray_image.jpg", gray)

    # Aplicando limiarização
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("thresholded_image.jpg", threshold)

    return threshold