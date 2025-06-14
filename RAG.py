'''
RETRIEVAL AUGMENTED GENERATION (RAG) MODULE
This module provides functionality to split text into manageable chunks, create or update a FAISS vector store,
and manage embeddings for a RAG pipeline.
'''

import os
import re
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import ollama

# Configuration
MODEL_NAME = "all-MiniLM-L6-v2"  # Lightweight embedding model
LLM_MODEL_NAME = "deepseek-r1:8b"  # DeepSeek R1 model for response generation
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Character overlap for context continuity

# RAG Parameters
top_k = 5  # Number of top relevant chunks to retrieve for each LLM call
depth = 1  # Number of retrieval iterations: 1 to 3. The higher, the more search extent, but processing time multiplies. E.g. if top_k = 5 and depth = 2, the LLM will retrieve the top 5 chunks from the vector store in a prompt, then the next 5, and use them to generate a response.
max_context_length = 3000  # Maximum length of context to pass to the LLM for each prompt, from collating the top chunks

# Prompt parameters
temperature = 0.3  # Temperature for response generation (creativity)
prompt_text = '''Provide a clear and concise response, quoting the exact text from the context as evidence and including the source references in the format [Source: filename].'''
max_tokens = 500  # Maximum tokens for the response generation (output length)

# Prepare text in chunks
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

# Create vector store
def load_or_create_vector_store(directory, txt_folder, vector_store_subfolder="vector_store"):
    """
    Create a FAISS vector store from .txt files in the specified folder.
    The vector store is saved in a subfolder within txt_folder.
    This function regenerates the vector store from scratch.
    
    Args:
        txt_folder (str or Path): Folder containing .txt files.
        vector_store_subfolder (str): Subfolder name for vector store (default: 'vector_store').
    
    Returns:
        FAISS: Vector store object, or None if no valid files are found.
    """
    txt_folder = Path(f"{directory}{txt_folder}")
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

    # Create new vector store
    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    print(f"Created new vector store with {len(texts)} chunks at {vector_store_path}.")

    # Save to disk
    vector_store.save_local(vector_store_path)
    print(f"Saved vector store to {vector_store_path}")
    return vector_store

# Query the vector store
def embed_query(query: str, model_name: str = "all-MiniLM-L6-v2") -> list: # Convert query to embedding using HuggingFaceEmbeddings
    """Convert query to embedding using HuggingFaceEmbeddings."""
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    query_embedding = embeddings.embed_query(query)
    return query_embedding

def retrieve_chunks(query: str, vector_store_path: str, k: int = depth*top_k) -> list: # Retrieve top-k relevant chunks from FAISS vector store, considering depth for multiple calls
    """Retrieve top-k relevant chunks from FAISS vector store."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
    query_embedding = embed_query(query)
    results = vector_store.similarity_search_by_vector(query_embedding, k=k)
    retrieved_chunks = [{"text": doc.page_content, "source": doc.metadata["source"]} for doc in results]
    return retrieved_chunks

def assemble_context(chunks: list, max_context_length: int = max_context_length) -> str:# Combine retrieved chunks into a context string
    """Combine retrieved chunks into a context string with source references."""
    formatted_chunks = [f"[Source: {chunk['source']}] {chunk['text']}" for chunk in chunks]
    context = "\n\n".join(formatted_chunks)
    if len(context) > max_context_length:
        context = context[:max_context_length]
    return context

def generate_response(
        query: str, 
        context: str, 
        prompt: str = prompt_text, 
        model_name: str = LLM_MODEL_NAME, 
        temperature: float = temperature,
        max_tokens: int = max_tokens,
        show_thinking: bool = False
        ) -> str:
    """Generate response using DeepSeek via Ollama with query and context."""
    # Create prompt with instructions
    if show_thinking:
        thinking_prompt = """First, explain your reasoning step-by-step in a <think> section. Then, provide the answer as specified below."""
        full_prompt = f"""Context:
{context}

Query:
{query}

Answer:
{thinking_prompt}

{prompt}
"""
    else:
        full_prompt = f"""Context:
{context}

Query:
{query}

Answer:
{prompt}
"""
    
    # Call Ollama to generate response
    response = ollama.generate(
        model=model_name,
        prompt=full_prompt,
        options={
            "temperature": temperature,  # Low temperature for precise quoting
            "max_tokens": max_tokens  # Limit output length
        }
    )
    
    # Extract the generated answer
    answer = response.get("response", "").strip()
    
    # Remove <think> section if show_thinking is False
    if not show_thinking:
        answer = re.sub(r'<think>.*?</think>\s*', '', answer, flags=re.DOTALL)
    
    return answer

# Main RAG pipeline function
def rag_pipeline(
    query: str,
    vector_store_path: str,
    k: int = top_k,
    depth: int = depth,
    max_context_length: int = max_context_length,
    prompt: str = prompt_text,
    model_name: str = LLM_MODEL_NAME,
    show_thinking: bool = False,
    temperature: float = temperature,
    max_tokens: int = max_tokens
) -> str:
    """Execute the full RAG pipeline with iterative depth for multiple prompts."""
    # Validate inputs
    if depth < 1:
        depth = 1
    # if k < 1:
    #     k = top_k
    
    # Retrieve k * depth chunks
    total_chunks = k * depth
    chunks = retrieve_chunks(query, vector_store_path, k=total_chunks)
    print(f"Retrieved {len(chunks)} chunks for query: '{query}'")
    
    # Split chunks into batches of k
    chunk_batches = [chunks[i:i+k] for i in range(0, len(chunks), k)]
    
    # Process each batch with a separate prompt
    responses = []
    seen_chunks = set()
    for batch in chunk_batches:
        if not batch:
            continue
        context = assemble_context(batch, max_context_length=max_context_length)
        print(f"Assembled context for batch: {context[:100]}...")  # Show first 100 chars of context for debugging
        response = generate_response(
            query=query,
            context=context,
            prompt=prompt,
            model_name=model_name,
            show_thinking=show_thinking,
            temperature=temperature,
            max_tokens=max_tokens
        )
        print(f"Generated response for batch: {response[:100]}...")
        # Extract evidence (bullet-point format assumption was wrong)
        evidence_lines = [line.strip() for line in response.split('\n')] # if line.strip().startswith('-')]
        for line in evidence_lines:
            chunk_text = line.split('[Source:')[0].strip().strip('-').strip()
            if chunk_text not in seen_chunks:
                seen_chunks.add(chunk_text)
                responses.append(line)
    
    # Combine responses
    if not responses:
        return "No relevant evidence found."
    final_response = f"\n".join(responses)
    return final_response



