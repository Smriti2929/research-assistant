import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title= "Research Assistant",
    page_icon= "📚",
    layout = "wide"
)

#Session State

if "messages" not in st.session_state:
    st.session_state.messages = []

documents = []

# Craeting Sidebar

with st.sidebar:
    st.title("📚 Research Assistant")
    st.markdown("""
Built with:
- FastAPI
- FAISS
- Sentence Transformers
- Gemini
- Streamlit 
""")
    st.metric(
        "Documents",
        len(documents)
    )

    st.metric (
        "Messages",
        len(
            st.session_state.messages
        )
    )
    
    if st.button(
        "🗑️ Clear Chat"
    ):
        st.session_state.messages = []
        st.rerun()

    chat_text = ""

    for msg in st.session_state.messages:
        chat_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n\n"
        )

    st.download_button(
        label = "📥 Export Chat",
        data = chat_text,
        file_name= "chat_history.txt",
        mime= "text/plain"
    )        

    st.write(
        f"Messages: {len(st.session_state.messages)}"
    )    
    
    st.divider()
    st.subheader(
        "Uploaded Documents"
    )

    try:

        response = requests.get(
            f"{API_URL}/documents"
        )

        if response.status_code == 200:

            result = response.json()
            documents = result [
                "documents"
            ]
            st.write(
                f"Documents: {result['count']}"
            )

            for doc in documents:
                st.write(
                    f"📄 {doc}"
                )
    except:

        st.warning(
            "Backend not running"
        )

# Main Title                    

st.title("📚 RAG Research Assistant")
st.write(
    "Upload documents and chat with them."
)

#Upload Section
st.subheader(
    "Upload PDF"
)

uploaded_file = st.file_uploader(
    "Choose PDF",
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
            f"{uploaded_file.name} uploaded"
        )

#Document Section

if documents:

    selected_doc = st.selectbox(
        "Select Document",
        documents
    )

# CHat History    
st.divider()

st.subheader("Chat") 

for message in st.session_state.messages:
    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )

#Chat I/p

if documents:
    prompt = st.chat_input(
        "Ask a question ..."
    )
    if prompt:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message(
            "user"
        ):
            st.markdown(prompt)

        payload = {
            "file_name": selected_doc,
            "question": prompt,
            "chat_history": st.session_state.messages
        }

        response = requests.post(
            f"{API_URL}/ask",
            json= payload
        ) 

        if response.status_code == 200:
            result = response.json()

            answer = result[
                "answer"
            ]

            confidence = result.get(
                "confidence",
                0
            ) 

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            ) 

            with st.chat_message(
                "assistant"
            ):
                st.markdown(
                    answer
                )

                st.caption(
                    f"Confidence: {confidence}%"
                )

                if "sources" in result:

                    with st.expander(
                        "Sources"
                    ):
                        if "documents" in result:
                            st.markdown(
                                "### Documents Used"
                            )

                            for doc in result[
                                "documents"
                            ]:
                                st.write(
                                    f"📄 {doc}"
                                )
                                
                        for i, source in enumerate(
                            result["sources"],
                            start = 1
                        ):
                            st.markdown(
                                f"### Source {i}"
                            )

                            st.code(
                                source,
                                language = "text"
                            )



