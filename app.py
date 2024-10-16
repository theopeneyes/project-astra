
import streamlit as st
import tempfile 
import os


# Streamlit UI
st.title("PDF Uploader")

# File uploader component
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

# If a file is uploaded
if uploaded_pdf is not None:
    with tempfile.TemporaryDirectory() as temp_dir: 
        file_path = os.path.join(temp_dir, uploaded_pdf.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        