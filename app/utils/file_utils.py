import json

def save_chunks(chunks, file_path):

    with open(
        file_path,
        "w",
        encoding= "utf-8"
    ) as f:
        
        json.dump(
            chunks,
            f,
            ensure_ascii= False,
            indent=4
        )