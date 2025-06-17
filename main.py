'''
Main script to process documents, create a vector store, and run a RAG pipeline for querying.
This script handles the extraction of text from various file formats, creates a vector store for efficient querying,
and allows for querying the vector store using a RAG (Retrieval-Augmented Generation) pipeline.

Author: Cristina Sanchez
v1 2025-06-14'''

# ---------------------------------------------- #
# ---------------- Dependencies ---------------- #
# ---------------------------------------------- #

from fileprocessing import extract_text_from_file, extract_text_from_directory
import os
import json
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from RAG import load_or_create_vector_store, rag_pipeline
from structure_output import parse_llm_output_to_df

# ---------------------------------------------- #
# ------------------- Inputs ------------------- #
# ---------------------------------------------- #

directory = "INPUT/"  # Replace with your directory path
text_directory = "text_processing"  # Subdirectory for .txt files
vector_subdirectory = "vector_store"  # Subdirectory for vector store
# OCR Mode: Choose if pdfs are processed from their text only (faster) or transfored to images and OCR (slower but includes images)
ocr_mode = False # Set to True if you want to use OCR for PDFs
regenerate_vector_store = False  # Set to True to regenerate the vector database e.g. after adding new files

# Note: additional prompt and RAG parameters in RAG.py

query = '''Is the military capability need and/or business capability need (inc. Transformation) suitably evidenced and prioritised within departmental planning?'''

# ---------------------------------------------- #
# --------------- Main Functions --------------- #
# ---------------------------------------------- #

# Function to process files and create the vector store
def RAG_base(directory, txt_folder=text_directory, vector_store_subfolder=vector_subdirectory):
    """
    Main function to process files, create vector store, and query it.
    
    Args:
        directory (list of str or Path): Directory of input files.
        txt_folder (str): Folder for .txt files (default: 'text_files').
        vector_store_subfolder (str): Subfolder for vector store (default: 'vector_store').
    """

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

# Query function for RAG pipeline
def run_rag_pipeline(query, directory, text_directory=text_directory, vector_subdirectory=vector_subdirectory):
    vector_store_path = f"{directory}/{text_directory}/{vector_subdirectory}"
    print(f"Querying: {query}")
    response = rag_pipeline(query, directory=directory, text_directory=text_directory, vector_store_path=vector_store_path, show_thinking=False)
    print(f"RAG pipeline response:\n{response}\n")
    return response

# ---------------------------------------------- #
# --------------- Main Execution --------------- #
# ---------------------------------------------- #

# Process the documents and create/update the vector store if selected (in Inputs)
if regenerate_vector_store:
    print("Regenerating vector database...")
    RAG_base(directory, txt_folder=text_directory, vector_store_subfolder=vector_subdirectory)
else:
    pass

# Save response as txt
response = run_rag_pipeline(query = query, directory=directory, text_directory=text_directory, vector_subdirectory=vector_subdirectory)
print(response)
# Save the run rag pipeline response to a .txt file
output_file = f"{directory}/{text_directory}/rag_response.txt"
def write_output(output_file, query, response):
    with open(output_file, "w") as f:
        f.write(f"Query: {query}\n")
        f.write("RAG pipeline response:\n")
        f.write(response)

# write_output(output_file, query, response)
df = parse_llm_output_to_df(query, response)
df.head()
df.to_csv(f"{directory}/{text_directory}/rag_response.csv", index=False)


