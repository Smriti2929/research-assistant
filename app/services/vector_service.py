import faiss
import numpy as np

def build_faiss_index(embeddings):

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(
        dimension
    )

    vectors = np.array(
        embeddings,
        dtype= "float32"
    )

    index.add(vectors)

    return index

def save_faiss_index(index, path):

    faiss.write_index(
        index,
        path
    )