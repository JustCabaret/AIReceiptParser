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
- **Database**: MySQL
- **AI Integration**: OpenAI GPT-4 API
- **OCR**: Tesseract

## Getting Started

### Prerequisites

- Python 3.10 or higher
- MySQL Server (8.0+)
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

4. **Create the MySQL database:**
   - Run the following SQL script on your MySQL server:
     ```sql
     CREATE DATABASE receiptparserdb;
     USE receiptparserdb;
     
     CREATE TABLE receipts (
         id INT AUTO_INCREMENT PRIMARY KEY,
         total INT NOT NULL,
         source VARCHAR(255) NOT NULL,
         parsed_at DATETIME DEFAULT CURRENT_TIMESTAMP
     );

     CREATE TABLE receipt_items (
         id INT AUTO_INCREMENT PRIMARY KEY,
         receipt_id INT NOT NULL,
         product VARCHAR(255) NOT NULL,
         quantity INT NOT NULL,
         price INT NOT NULL,
         category VARCHAR(50) DEFAULT NULL,
         FOREIGN KEY (receipt_id) REFERENCES receipts(id)
     );
     ```

5. **Update the database credentials:**
   Edit `database.py` with your MySQL connection details:
   ```python
   mysql.connector.connect(
       host="127.0.0.1",
       user="your_username",
       password="your_password",
       database="receiptparserdb"
   )
   ```

6. **Run the application:**
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
