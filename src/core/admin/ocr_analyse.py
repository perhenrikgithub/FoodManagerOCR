from typing import NamedTuple
import pytesseract
import openai
from PIL import Image


class Items(NamedTuple):
    start_text: str
    end_text: str


STORE_DICT = {
    "rema 1000": Items(start_text="serienr", end_text="sum "),
    "coop": Items(start_text="ref", end_text="totalt"),
}


def _export_image_text(image_path: str) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang="nor").lower()


def make_gpt_prompt(image_path: str) -> str:
    text = _export_image_text(image_path)
    lines = text.split("\n")
    store = STORE_DICT[lines[0]]

    start_index = 0
    end_index = 0

    for i, line in enumerate(lines):
        if not start_index and (line.startswith(store.start_text)):
            start_index = i + 1
        elif not end_index and line.startswith(store.end_text):
            end_index = i
            break

    return "\n".join(lines[start_index:end_index])


def main() -> None:
    print(make_gpt_prompt("src/receipts/receipt.jpg"))
    # print(make_gpt_prompt("src/receipts/coop_obs.jpeg"))


if __name__ == "__main__":
    main()
