import streamlit as st
import os
from fileprocessing import extract_text_from_directory
from RAG import load_or_create_vector_store, rag_pipeline
from PIL import Image  # For loading the header image
from pathlib import Path


# Initialize session state
if "reset" not in st.session_state:
    st.session_state.reset = False

# Query - to be linked to the same as main.py
query = "Is the military capability gap and/or business capability gap to be addressed suitably defined?"

# Header image
try:
    header_image = Image.open("logo.png")  # Replace with your image path
    st.image(header_image, use_container_width=True)
except FileNotFoundError:
    st.warning("Header image not found. Please add 'logo.png' to the project directory.")

# Title and subheader
st.title("DeepSeek R1 Query Interface")
st.markdown(
    """
    **Version**: v1, 2025-06-14  
    **Author**: Cristina Sanchez  
    **Description**: This application processes documents in a specified folder, converts them to text, creates a vector store, and queries a DeepSeek R1 8b model using a Retrieval-Augmented Generation (RAG) pipeline to provide relevant answers - all with a **local** setup, no cloud.
    **Files supported**: pdf, docx, xlsx, txt, csv, pptx, and images (png, jpg, jpeg) for now.
     """,
    unsafe_allow_html=True
)

# Reset button
if st.button("Reset"):
    st.session_state.directory = "INPUT/"
    st.session_state.ocr_mode = False
    st.session_state.query = query
    st.session_state.reset = True
    st.rerun()  # Refresh the app to reflect cleared inputs

# Input for directory
raw_path = st.text_input(
    "Enter or paste folder path:",
    value=st.session_state.get("directory", "INPUT/"),
    key="raw_path"
)
# Sanitize the input path
sanitized_path = None
try:
    sanitized_path = str(Path(raw_path).resolve())  # Normalize \ to / and validate
    # Ensure trailing slash
    if not sanitized_path.endswith(os.sep):
        sanitized_path += os.sep
    st.session_state.directory = sanitized_path
    st.write(f"Sanitised path: {sanitized_path}")
except (ValueError, OSError):
    st.error("Invalid folder path. Please enter a valid directory.")
    st.session_state.directory = "INPUT/"  # Fallback to default
directory = st.session_state.directory
text_directory = "text_processing"
vector_subdirectory = "vector_store"

# OCR checkbox with hover tooltip
st.markdown(
    """
    <div title="When checked, PDFs are processed using Optical Character Recognition (OCR) to extract text from images within the PDFs. This is slower but includes text from images. When unchecked, only embedded text in PDFs is extracted (faster).">
        Use text recognition for PDFs ⓘ 
    </div>
    """,
    unsafe_allow_html=True
)
ocr_mode = st.checkbox("", value=st.session_state.get("ocr_mode", True), key="ocr_mode")

st.write(f"File processing run only needed when files are added.")

# Button to process files
if st.button("Process Files"):
    if os.path.exists(directory):
        with st.spinner("Processing files and creating indexing..."):
            extract_text_from_directory(directory, ocr_mode=ocr_mode, txt_processing_dir=text_directory)
            vector_store = load_or_create_vector_store(
                directory=directory,
                txt_folder=text_directory,
                vector_store_subfolder=vector_subdirectory
            )
            if vector_store:
                st.success("Files processed and indexing created!")
            else:
                st.error("Failed to create indexing.")
    else:
        st.error("Invalid directory path!")

# Input for query
query = st.text_area(
    "Enter your query:",
    value=st.session_state.get("query", query)
)

# Button to submit query
if st.button("Submit Query"):
    vector_store_path = os.path.join(directory, text_directory, vector_subdirectory)
    if query.strip() and os.path.exists(vector_store_path):
        with st.spinner("Querying model..."):
            response = rag_pipeline(query, vector_store_path, directory, text_directory, show_thinking=False)
            st.subheader("Model Response:")
            st.markdown(response, unsafe_allow_html=True)
    elif not query.strip():
        st.error("Please enter a query!")
    else:
        st.error("Vector store not found! Process files first.")