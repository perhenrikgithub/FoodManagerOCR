import pytesseract
from PIL import Image


def export_image_text(image_path: str) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang="nor")


def main() -> None:
    print(export_image_text("src/receipts/receipt.jpg"))


if __name__ == "__main__":
    main()
