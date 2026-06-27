from app.services.gemini_service import ask_gemini

response = ask_gemini(
    "Explain Retrieval Augmented Generation in 3 simple sentences."
)

print(response)