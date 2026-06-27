import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title= "Research Assistant",
    page_icon= "📚",
    layout = "wide"
)

st.title("📚 Research Assistant")
st.write(
    "Upload PDFs and ask questions."
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type= ["pdf"]
)

if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
        )
    }

    response = requests.post(
        f"{API_URL}/upload",
        files= files
    )

    if response.status_code == 200:

        st.success(
            "PDF uploaded successfully!"
        )

        st.json(
            response.json()
        )
    else:
        st.error(
            "Upload failed."
        )

st.divider()

st.header("Uploaded Documents") 

documents = []

try:

    response = requests.get(
        f"{API_URL}/documents"
    )

    if response.status_code == 200:
        result = response.json()

        documents = result[
            "documents"
        ]

        st.write(
            f"Total Documents: {result['count']}"
        )
        for doc in documents:
            st.write(
                f"📄 {doc}"
            )

except Exception as e:
    
    st.error(
        f"Could not load documents: {e}"
    )

#searching single document 

st.divider()

st.header("Ask a Single Document")

if documents:

    selected_doc = st.selectbox(
        "Selected a document",
        documents
    )

    question = st.text_input(
        "Enter your question"
    )

    if st.button(
        "Ask Document"
    ):
        payload = {
            "file_name": selected_doc,
            "question": question
        }

        response = requests.post(
            f"{API_URL}/ask",
            json = payload
        )

        if response.status_code == 200:

            result = response.json()

            st.subheader(
                "Answer"
            )

            st.success(
                result["answer"]
            )

            st.subheader(
                "Retrieved Sources"
            )

            for source in result[
                "sources"
            ]:
                
                st.info(
                    source
                )
        else:

            st.error(
                "Question failed."
            )
    else:
        st.warning(
            "Upload a PDF first."
        )        

# Searching Multiple documents 

st.divider()

st.header(
    "Search Across All Docuemnts"
)

global_question = st.text_input(
    "Ask a question across all uploaded documents"
)

if st.button(
    "Search All Documents"
):
    response = requests.post(
        f"{API_URL}/ask-all",
        json= {
            "question": global_question
        }
    )

    if response.status_code == 200:

        result = response.json()

        st.subheader(
            "Answer"
        )

        st.success(
            result["answer"]
        )

        st.write(
            f"Documents searched: {result['document_searched']}"
        )
    else:
        st.error(
            "Search failed."
        )    