import json
import os

def save_chunks(chunks, file_path):

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok= True
    )

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