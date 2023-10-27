import ast
import timeit
from typing import NamedTuple
import pytesseract
import openai
from PIL import Image

from hidden_constants import OPENAI_API_KEY


class Item(NamedTuple):
    start_text: str
    end_text: str


STORE_DICT = {
    "rema 1000": Item(start_text="serienr", end_text="sum "),
    "coop obs": Item(start_text="ref", end_text="totalt "),
    "coop extra": Item(start_text="salgskvittering", end_text="totalt "),
    "unknown": Item(start_text="unknown", end_text="unknown"),
}


def _export_image_text(image_path: str) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang="nor").lower()


def _make_gpt_prompt(image_path: str) -> str:
    lines = _export_image_text(image_path).split("\n")

    store = lines[0]
    if "extra" in store:
        store = "coop extra"
    elif "obs" in store:
        store = "coop obs"
    elif "rema" in store:
        store = "rema 1000"
    else:
        store = "unknown"

    store = STORE_DICT[store]

    start_index = 0
    end_index = len(lines)

    for i, line in enumerate(lines):
        if not start_index and line.startswith(store.start_text):
            start_index = i + 1
        elif not end_index and line.startswith(store.end_text):
            end_index = i
            break

    return ", ".join(lines[start_index:end_index])


def make_gpt_request(image_path: str) -> list[dict[str, str | int]]:
    message_prefix = (
        "Lag et JSON-datasett fra følgende matvarer. Inkluder matvare, "
        "antall (standard=1), vekt (standard=N/A) og kategori (kjøleskap/"
        "tørrvare/fryser). Ignorer pris. Rett opp i skrivefeil og generaliser "
        "navnet på matvaren."
    )
    prompt = _make_gpt_prompt(image_path)

    openai.api_key = OPENAI_API_KEY
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{message_prefix}:\n{prompt}"}],
    )

    result = completion.choices[0].message.content  # type: ignore
    result = ast.literal_eval(result[result.find("[") : result.rfind("]") + 1])
    print(result)
    return result


def main() -> None:
    test_receipts = {
        "rema": "src/receipts/rema_1000.jpg",
        "obs": "src/receipts/coop_obs.jpeg",
        "extra": "src/receipts/coop_extra.jpg",
    }
    print(
        timeit.timeit(
            "make_gpt_request(test_receipts['extra'])",
            globals=globals() | locals(),
            number=1,
        )
    )


if __name__ == "__main__":
    main()
