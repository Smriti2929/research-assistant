import os

def get_uploaded_documents():

    if not os.path.exists("uploads"):
        return []

    documents = []

    for file in os.listdir("uploads"):

        if file.endswith("pdf"):
            documents.append(file)

    return documents            