'''
This module provides functionality to split text into manageable chunks, create or update a FAISS vector store,
and manage embeddings for a RAG pipeline.
'''

import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configuration
MODEL_NAME = "all-MiniLM-L6-v2"  # Lightweight embedding model
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Character overlap for context continuity

def read_text_file(file_path):
    """Read a text file and return its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def split_text(text, source_file):
    """Split text into chunks with metadata for RAG."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_text(text)
    return [{"text": chunk, "source": source_file} for chunk in chunks]

def load_or_create_vector_store(txt_folder, vector_store_subfolder="vector_store"):
    """
    Create a FAISS vector store from .txt files in the specified folder.
    The vector store is saved in a subfolder within txt_folder.
    This function always regenerates the vector store from scratch.
    
    Args:
        txt_folder (str or Path): Folder containing .txt files.
        vector_store_subfolder (str): Subfolder name for vector store (default: 'vector_store').
    
    Returns:
        FAISS: Vector store object, or None if no valid files are found.
    """
    txt_folder = Path(txt_folder)
    vector_store_path = txt_folder / vector_store_subfolder
    
    if not txt_folder.exists():
        print(f"Text folder {txt_folder} does not exist. Creating it.")
        txt_folder.mkdir(parents=True, exist_ok=True)

    # Ensure the vector store folder exists
    if not vector_store_path.exists():
        print(f"Vector store folder {vector_store_path} does not exist. Creating it.")
        vector_store_path.mkdir(parents=True, exist_ok=True)

    # Collect chunks from all .txt files
    all_chunks = []
    for file_path in txt_folder.glob("*.txt"):
        text = read_text_file(file_path)
        if text:
            chunks = split_text(text, source_file=file_path.name)
            all_chunks.extend(chunks)
    
    if not all_chunks:
        print(f"No valid text files found in {txt_folder}.")
        return None

    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    
    # Prepare texts and metadata
    texts = [chunk["text"] for chunk in all_chunks]
    metadatas = [{"source": chunk["source"]} for chunk in all_chunks]

    # Always create new vector store
    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    print(f"Created new vector store with {len(texts)} chunks at {vector_store_path}.")

    # Save to disk
    vector_store.save_local(vector_store_path)
    print(f"Saved vector store to {vector_store_path}")
    return vector_store

def query_vector_store(vector_store, query, k=3):
    """
    Query the vector store and return relevant chunks with sources.
    
    Args:
        vector_store (FAISS): The FAISS vector store.
        query (str): The user query.
        k (int): Number of chunks to retrieve.
    
    Returns:
        tuple: (context, sources) where context is the combined text and sources is a list of source files.
               Returns (None, None) if vector_store is None.
    """
    if vector_store is None:
        print("No vector store provided.")
        return None, None
    
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    retrieved_docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    sources = [doc.metadata["source"] for doc in retrieved_docs]
    return context, sources
