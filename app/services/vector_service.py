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

def load_faiss_index(path):

    return faiss.read_index(path)

def search_index(
        index,
        query_embedding,
        top_k=5
):

    query_vector = np.array(
        [query_embedding],
        dtype= "float32"
    )

    distances, indices = index.search(
        query_vector,
        top_k
    )

    return indices[0]    