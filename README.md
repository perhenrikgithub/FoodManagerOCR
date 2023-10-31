# Receipt Text Extractor

This is a Python application that uses pytesseract to extract text from a receipt image and convert it to JSON format.

## Installation

1. Clone the repository: `git clone https://github.com/perhenrikgithub/reciept-ocr-backend.git`
2. Install the required packages: `pip3 install -r requirements.txt`

## Usage

1. Place the receipt image in the `src/receipts` folder.
2. Run the `src/core/ocr_analyse.py` script: `python3 src/core/ocr_analyse.py`
3. The extracted text will be saved in a JSON file in the `src/db` folder named `articles.json`.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
