import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI


# Helper functions
def fail(msg: str):
    """Show a user-friendly error and stop the Streamlit app (fast fail)."""
    st.error(msg)
    st.stop()


def get_api_key() -> str:
    """Load and validate API key (preventative if/raise style)."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        fail("Missing GOOGLE_API_KEY in .env (Fix: add GOOGLE_API_KEY=... to your .env file)")
    return api_key


def validate_data_dir(data_dir: str) -> Path:
    """#2 Test for a data directory"""
    p = Path(data_dir)
    if not p.exists():
        fail(f"Data directory not found: '{data_dir}'. (Fix: create a folder named '{data_dir}' and add files)")
    if not p.is_dir():
        fail(f"'{data_dir}' exists but is not a directory. (Fix: DATA_DIR must be a folder)")
    return p


def validate_has_files(data_path: Path) -> list[Path]:
    """#4 Test to make sure there are file(s) in the directory""" #new
    allowed = {".pdf", ".txt", ".md"}
    files = [x for x in data_path.iterdir() if x.is_file() and x.suffix.lower() in allowed]

    if not files:
        fail(f"No supported files in '{data_path}'. Add one of: {sorted(allowed)}")
    return files


# ---------- Cache heavy initialization ----------
@st.cache_resource(show_spinner="Building index (cached)...")
def build_query_engine(data_dir: str, api_key: str, fingerprint: str):
    """
    #3 Cache the data/index with Streamlit to reduce latency
    This is cached so Streamlit reruns won't rebuild the index every time.
    """
    # RAG engine init can fail → let caller handle via try/except (runtime protection)
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

    # --- #1 API key validation ---
    api_key = get_api_key()

    # --- #2 and #4 directory + file checks ---
    data_dir = "data"
    data_path = validate_data_dir(data_dir)
    _files = validate_has_files(data_path)

    def dir_fingerprint(data_path: Path) -> str:
        files = sorted([p for p in data_path.iterdir() if p.is_file()])
        stamp = [(p.name, p.stat().st_mtime_ns, p.stat().st_size) for p in files]
        return str(stamp)

    # --- #5 Wrap RAG engine init in try/except (fast fail) ---
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
        # --- #5 Wrap query in try/except (graceful runtime handling) ---
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
