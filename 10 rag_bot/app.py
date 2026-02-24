import os

import streamlit as st
from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI


@st.cache_resource
def build_query_engine(data_dir: str):
    docs = SimpleDirectoryReader(data_dir).load_data()
    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine(similarity_top_k=5)


def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("Missing GOOGLE_API_KEY in .env")
        st.stop()

    Settings.llm = GoogleGenAI(
        model="gemini-2.5-flash",
        api_key=api_key,
    )

    # 本地embedding（避免rate limit）
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    st.title("Babson Handbook RAG Chatbot")
    query_engine = build_query_engine("data")
    user_input = st.chat_input("Ask a handbook question")

    if user_input:
        with st.spinner("Thinking..."):
            response = query_engine.query(user_input)

        st.write(response.response)


if __name__ == "__main__":
    main()