import os
from pathlib import Path
from typing import List

import streamlit as st
from dotenv import load_dotenv

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()


# Helper functions
def fail(msg: str):
    """Show a user-friendly error and stop the Streamlit app (fast fail)."""
    st.error(msg)
    st.stop()


def get_api_key() -> str:
    """Validate API key."""
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        fail("Missing GOOGLE_API_KEY in .env (Fix: add GOOGLE_API_KEY=... to your .env file)")
    return api_key


def validate_data_dir(data_dir: str) -> Path:
    """Test whether the data directory exists and is a folder."""
    p = Path(data_dir)
    if not p.exists():
        fail(f"Data directory not found: '{data_dir}'. (Fix: create a folder named '{data_dir}' and add files)")
    if not p.is_dir():
        fail(f"'{data_dir}' exists but is not a directory. (Fix: DATA_DIR must be a folder)")
    return p


def validate_has_files(data_path: Path) -> List[Path]:
    """Test whether the data directory contains supported files."""
    allowed = {".pdf", ".txt", ".md"}
    files = [x for x in data_path.iterdir() if x.is_file() and x.suffix.lower() in allowed]

    if not files:
        fail(f"No supported files in '{data_path}'. Add one of: {sorted(allowed)}")
    return files


def dir_fingerprint(data_path: Path) -> str:
    """Create a fingerprint from filenames, modified times, and sizes."""
    files = sorted([p for p in data_path.iterdir() if p.is_file()])
    stamp = [(p.name, p.stat().st_mtime_ns, p.stat().st_size) for p in files]
    return str(stamp)


@st.cache_resource(show_spinner="Building index (cached)...")
def build_query_engine(data_dir: str, api_key: str, fingerprint: str):
    """
    Cache the RAG engine so Streamlit reruns do not rebuild the index every time.
    The fingerprint forces a rebuild when files in the directory change.
    """
    Settings.llm = GoogleGenAI(
        model="gemini-2.5-flash",
        api_key=api_key,
    )

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    docs = SimpleDirectoryReader(
        data_dir,
        required_exts=[".pdf", ".txt", ".md"]
    ).load_data()

    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine(similarity_top_k=5)


def main():
    st.title("Babson Handbook RAG Chatbot")

    api_key = get_api_key()

    data_dir = "data"
    data_path = validate_data_dir(data_dir)
    _files = validate_has_files(data_path)

    try:
        fingerprint = dir_fingerprint(data_path)
        query_engine = build_query_engine(data_dir, api_key, fingerprint)
    except Exception as e:
        fail(
            "RAG engine failed to initialize.\n\n"
            f"Details: {e}\n\n"
            "Fix ideas: check your data files, dependencies, and API key validity."
        )

    user_input = st.chat_input("Ask a handbook question")

    if user_input:
        try:
            with st.spinner("Thinking..."):
                response = query_engine.query(user_input)
            st.write(response.response)
        except Exception as e:
            fail(
                "Query failed while generating an answer.\n\n"
                f"Details: {e}\n\n"
                "Fix ideas: try a shorter question, check model/API limits, or verify your documents."
            )


if __name__ == "__main__":
    main()