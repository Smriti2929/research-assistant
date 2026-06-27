from app.services.embedding_service import get_embedding

embedding = get_embedding(
    "What is machine learning?"
)

print(len(embedding))