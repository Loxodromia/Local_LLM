from ollama_fn import process_file
from fileprocessing import read_csv, read_pdf, read_image, read_doc, read_docx, read_odt, read_ppt, read_pptx, read_txt, read_xls, read_excel
from fileprocessing import extract_text_from_file, extract_text_from_directory
import os
import json

from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from RAG import load_or_create_vector_store

# Input
directory = "INPUT/"  # Replace with your directory path
text_directory = "text_processing"  # Subdirectory for .txt files
vector_subdirectory = "vector_store"  # Subdirectory for vector store
# OCR Mode: Choose if pdfs are processed from their text only (faster) or transfored to images and OCR (slower but includes images)
ocr_mode = True  # Set to True if you want to use OCR for PDFs

# Main function to process files
def RAG_base(directory, txt_folder=text_directory, vector_store_subfolder=vector_subdirectory):
    """
    Main function to process files, create/update vector store, and query it.
    
    Args:
        directory (list of str or Path): Directory of input files.
        txt_folder (str): Folder for .txt files (default: 'text_files').
        vector_store_subfolder (str): Subfolder for vector store (default: 'vector_store').
    """
    # txt_folder = Path(txt_folder)
    
    # Step 1: Process input files to .txt
    extract_text_from_directory(directory, ocr_mode=ocr_mode, txt_processing_dir=text_directory)
    
    # Step 2: Create vector store
    vector_store = load_or_create_vector_store(
        directory=directory,
        txt_folder=txt_folder,
        vector_store_subfolder=vector_store_subfolder
    )
    if vector_store is None:
        print("Failed to create vector store. Exiting.")
        return

# Process the documents and create/update the vector store
# RAG_base(directory, txt_folder=text_directory, vector_store_subfolder=vector_subdirectory)


