import requests
import streamlit as st
from bs4 import BeautifulSoup

st.title("URL Content Extractor")
url = st.text_input("Enter a URL")

if st.button("Fetch Content"):
    if not url:
        st.error("Please enter a URL.")
    else:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()

            preview = text[:200]
            word_count = len(text.split())

            st.subheader("Preview")
            st.write(preview)

            st.subheader("Word Count")
            st.write(word_count)

        except Exception as e:
            st.error(f"Failed to fetch URL: {e}")
