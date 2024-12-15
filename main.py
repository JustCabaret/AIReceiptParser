import cv2
import pytesseract
import argparse
from modules.image_processing import preprocess_image
from modules.text_extraction import extract_text
from modules.gpt_processing import process_text_with_chatgpt

def main(image_path, api_key):
    # Pré-processar a imagem
    preprocessed_image = preprocess_image(image_path)

    # Extrair texto da imagem
    extracted_text = extract_text(preprocessed_image)

    # Enviar texto para o ChatGPT e obter dados estruturados
    structured_data = process_text_with_chatgpt(extracted_text, api_key)

    # Guardar os resultados num ficheiro JSON
    with open("receipt.json", "w") as json_file:
        json_file.write(structured_data)
        print("Dados guardados em receipt.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receipt Parser AI")
    parser.add_argument("image_path", type=str, help="Caminho da imagem da fatura")
    parser.add_argument("api_key", type=str, help="Chave da API OpenAI")

    args = parser.parse_args()
    main(args.image_path, args.api_key)