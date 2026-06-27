import os

def get_document_names():

    if not os.path.exists("uploads"):
        return []
    
    return [
        file
        for file in os.listdir("uploads")
        if file.endswith(".pdf")
    ]