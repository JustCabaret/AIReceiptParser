# AI Receipt Parser

This project provides an intelligent solution for automating the extraction and organization of data from receipt images. Designed for businesses and individuals, it simplifies the often tedious process of manual data entry, allowing users to focus on insights and decision-making. This application uses advanced OCR (Optical Character Recognition) technology and AI-driven processing to convert receipt images into well-organized, actionable data.

Inspired by @IAmTomShaw's [Receipt Vision](https://github.com/IAmTomShaw/receipt-vision).

## Features

- **Receipt Image Upload**: Users can upload images of receipts for automatic processing.
- **OCR Technology**: Text is extracted from the images using Tesseract OCR.
- **AI-Powered Parsing**: OpenAI's GPT-4 processes the extracted text into structured JSON data.
- **Database Integration**: Parsed data is stored in a MySQL database for persistence.
- **Web Interface**: A responsive interface to upload, view, and interact with receipts.
- **Receipt Details**: View breakdowns of individual receipts, including product details, prices, and categories.

## Preview

![image](https://github.com/user-attachments/assets/49f3a3d2-189c-4a63-855f-f43a43b69a0d)


## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite
- **AI Integration**: OpenAI GPT-4 API
- **OCR**: Tesseract

## Getting Started

### Prerequisites

- Python 3.10 or higher
- OpenAI API Key

### Installation

1. **Clone the repository to your local machine:**
   ```sh
   git clone https://github.com/JustCabaret/receipt-parser.git
   cd receipt-parser
   ```

2. **Set up the virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   - Create a copy of the `.env.example` file and rename it to `.env`:
     ```sh
     cp .env.example .env
     ```
   - Open the `.env` file and add your OpenAI API Key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

5. **Run the application:**
   - The SQLite database and tables will be created automatically on the first run.
   ```sh
   python app.py
   ```
   The server will run at `http://127.0.0.1:5000`.

## Usage

1. **Access the application:** Open `http://127.0.0.1:5000` in your browser.
2. **Upload Receipts:** Use the upload interface to submit receipt images.
3. **View Receipts:** Processed receipts will appear in the main table with their total and store name.
4. **View Details:** Click on any receipt to view its products, quantities, prices, and categories.

## API Endpoints

- **POST /process_receipt**: Uploads a receipt image and processes it.
  - Input: Image file and OpenAI API key
  - Output: Processed receipt data in JSON format
- **GET /receipts**: Retrieves all processed receipts.
- **GET /receipts/{receipt_id}**: Retrieves detailed information for a specific receipt.

## Example JSON Response

```json
{
    "total": 1250,
    "store": "SuperMart",
    "items": [
        {"product": "Milk", "quantity": 2, "price": 250, "type": "Groceries"},
        {"product": "Bread", "quantity": 1, "price": 150, "type": "Groceries"}
    ]
}
```

## Contributing

Feel free to fork the project, submit pull requests, report bugs, or suggest new features.

## Authors

- JustCabaret - [Your GitHub Profile](https://github.com/JustCabaret)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
