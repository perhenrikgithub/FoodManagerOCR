import pytesseract
from PIL import Image


def main() -> None:
    image = Image.open("src/receipts/receipt.jpg")
    print(pytesseract.image_to_string(image, lang="nor"))


if __name__ == "__main__":
    main()
