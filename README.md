# Receipt Parser

This project automates the extraction and organization of data from receipt images. It simplifies manual data entry by converting raw receipt images into structured JSON data and persistent local records.

Inspired by @IAmTomShaw's [Receipt Vision](https://github.com/IAmTomShaw/receipt-vision).

## Features

- **Image Processing**: Upload receipt images for automated text extraction using Tesseract OCR.
- **Language Model Parsing**: OpenAI's GPT-4 processes the raw OCR text into strict, structured JSON formatting.
- **Mock Testing Mode**: Bypass external API calls and Tesseract processing by using the built-in `test` API key, enabling rapid local UI development.
- **Data Export**: Export parsed receipt details (products, quantities, prices, categories) directly to standard CSV format.
- **Local Storage**: Parsed data is securely stored in a lightweight SQLite database.
- **Responsive Interface**: A clean, minimalistic web interface for uploading, viewing, and exporting receipts on any device.

## Preview

![image](https://github.com/user-attachments/assets/49f3a3d2-189c-4a63-855f-f43a43b69a0d)

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Database**: SQLite
- **External APIs**: OpenAI API
- **OCR Engine**: Tesseract

## Getting Started

### Prerequisites

- Python 3.10 or higher
- OpenAI API Key (or use `test` for mock data)
- Tesseract OCR installed on your system (optional if using mock mode)

### Installation

1. **Clone the repository:**
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

4. **Environment Configuration:**
   - Create a copy of the `.env.example` file and rename it to `.env`:
     ```sh
     cp .env.example .env
     ```
   - Open the `.env` file and set your API Key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

5. **Run the application:**
   - The SQLite database and tables will be initialized automatically on the first run.
   ```sh
   python backend/app.py
   ```
   The application servers will be available at `http://127.0.0.1:5000` (API) and `http://127.0.0.1:8000` (Frontend).

## Usage

1. **Access the application:** Open `http://127.0.0.1:8000` in your browser.
2. **Configure Authentication:** Click "API Key" to input your token. You can enter the word `test` to simulate backend processing without consuming API credits.
3. **Upload Receipts:** Submit images through the upload modal.
4. **View & Export:** Click on any parsed receipt row to view the line-item breakdown, and use the "Export CSV" button to download the data.

## API Endpoints

- **POST /process_receipt**: Uploads and processes a receipt image.
  - Input: `multipart/form-data` (Image file, API key)
  - Output: Processed receipt data in JSON format
- **GET /receipts**: Retrieves all processed receipts.
- **GET /receipts/{receipt_id}**: Retrieves line-item details for a specific receipt.

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
