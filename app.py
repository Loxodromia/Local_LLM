import streamlit as st
import os
from fileprocessing import extract_text_from_directory
from RAG import load_or_create_vector_store, rag_pipeline
from PIL import Image  # For loading the header image

# Initialize session state
if "reset" not in st.session_state:
    st.session_state.reset = False

# Header image
try:
    header_image = Image.open("logo.png")  # Replace with your image path
    st.image(header_image, use_container_width=True)
except FileNotFoundError:
    st.warning("Header image not found. Please add 'header_image.png' to the project directory.")

# Title and subheader
st.title("DeepSeek R1 Query Interface")
st.markdown(
    """
    **Version**: v1, 2025-06-14  
    **Author**: Cristina Sanchez  
    **Description**: This application processes documents in a specified folder, converts them to text, creates a vector store, and queries a local DeepSeek R1 8b model using a Retrieval-Augmented Generation (RAG) pipeline to provide relevant answers.
    """,
    unsafe_allow_html=True
)

# Reset button
if st.button("Reset"):
    st.session_state.directory = "INPUT/"
    st.session_state.ocr_mode = True
    st.session_state.query = "Show evidence of lessons learned from rainscreen cladding."
    st.session_state.reset = True
    st.rerun()  # Refresh the app to reflect cleared inputs

# Input for directory
directory = st.text_input(
    "Enter the reference folder path:",
    value=st.session_state.get("directory", "INPUT/")
)
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

# Button to process files
if st.button("Process Files"):
    if os.path.exists(directory):
        with st.spinner("Processing files and creating vector store..."):
            extract_text_from_directory(directory, ocr_mode=ocr_mode, txt_processing_dir=text_directory)
            vector_store = load_or_create_vector_store(
                directory=directory,
                txt_folder=text_directory,
                vector_store_subfolder=vector_subdirectory
            )
            if vector_store:
                st.success("Files processed and vector store created!")
            else:
                st.error("Failed to create vector store.")
    else:
        st.error("Invalid directory path!")

# Input for query
query = st.text_area(
    "Enter your query:",
    value=st.session_state.get("query", "Show evidence of lessons learned from rainscreen cladding.")
)

# Button to submit query
if st.button("Submit Query"):
    vector_store_path = os.path.join(directory, text_directory, vector_subdirectory)
    if query.strip() and os.path.exists(vector_store_path):
        with st.spinner("Querying model..."):
            response = rag_pipeline(query, vector_store_path, show_thinking=False)
            st.subheader("Model Response:")
            st.write(response)
    elif not query.strip():
        st.error("Please enter a query!")
    else:
        st.error("Vector store not found! Process files first.")