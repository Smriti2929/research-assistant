import json

def load_chunks(file_name):

    with open(
        f"data/{file_name}.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f) 