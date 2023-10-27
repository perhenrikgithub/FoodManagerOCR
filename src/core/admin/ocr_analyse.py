import ast
import timeit
from typing import NamedTuple
import pytesseract
import openai
from PIL import Image


OPENAI_API_KEY = "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"
# OPENAI_API_KEY = ""


class Items(NamedTuple):
    start_text: str
    end_text: str


STORE_DICT = {
    "rema 1000": Items(start_text="serienr", end_text="sum "),
    "coop": Items(start_text="ref", end_text="totalt"),
    "extra": Items(start_text="salgskvittering", end_text="totalt"),
}


def _export_image_text(image_path: str) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang="nor").lower()


def _make_gpt_prompt(image_path: str) -> str:
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

    return ", ".join(lines[start_index:end_index])


def make_gpt_request(image_path: str) -> list[dict[str, str | int]]:
    prompt = _make_gpt_prompt(image_path)
    message_prefix = (
        "Lag et JSON-datasett fra følgende matvarer. Inkluder matvare, "
        "antall (standard=1), vekt (standard=N/A) og kategori (kjøleskap/"
        "tørrvare/fryser). Ignorer pris. Fjern skrivefeil og generaliser "
        "navnet på matvaren."
    )
    openai.api_key = OPENAI_API_KEY
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{message_prefix}:\n{prompt}"}],
    )
    result = completion.choices[0].message.content  # type: ignore
    print(result)
    return ast.literal_eval(result)


def main() -> None:
    print(
        timeit.timeit(
            "print(make_gpt_request('src/receipts/receipt.jpg'))",
            globals=globals(),
            number=1,
        )
    )
    # print(make_gpt_request("src/receipts/coop_obs.jpeg"))


if __name__ == "__main__":
    main()
