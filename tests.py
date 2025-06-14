import ollama
from fileprocessing import read_csv, read_pdf, read_image, read_doc, read_docx, read_odt, read_ppt, read_pptx, read_txt, read_xls, read_excel
from fileprocessing import extract_text_from_file, extract_text_from_directory
from RAG import load_or_create_vector_store, embed_query, retrieve_chunks, assemble_context, generate_response, rag_pipeline
import os
import pytesseract

# Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
# print(pytesseract.image_to_string(Image.open(f'{directory}sample.jpg')))

# Input
directory = "INPUT/"  # Replace with your directory path
text_directory = f"text_processing"  # Subdirectory for .txt files
vector_directory = f"{text_directory}/vector_store"  # Directory for vector store

#----------------------------------
# CHECKS
#----------------------------------

# Embeddings model loading
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer("all-MiniLM-L6-v2")
# print("Model loaded successfully!")

# # Single file samples by extension
# print(read_pptx(f'{directory}guidance.pptx'))
# print(read_excel(f'{directory}Reqs.xlsx'))
# print(read_docx(f'{directory}RFP - SOR.docx'))
# print(read_txt(f'{directory}tbc.txt'))
# print(read_pdf(f'{directory}Sign-in & Set-up MFA.pdf'))

# # General file reading
# file_text = extract_text_from_file(f'{directory}guidance.pptx', ocr_mode=False, troubleshoot=True)
# print(file_text)

# # Process files in a directory
# print(extract_text_from_directory(directory, ocr_mode=False, troubleshoot=True))

# Main function to process files into txt
def main():
    """Main function to extract text from files or directories."""
    mode = input("Process a single file or all files in a directory? (single/directory): ").lower()
    ocr_mode = input("Process PDFs with full OCR (captures diagrams, slower)? (yes/no): ").lower() == 'yes'

    if mode == 'single':
        file_path = input("Enter the file path: ")
        result = extract_text_from_file(file_path, txt_processing_dir=text_directory, ocr_mode=ocr_mode)
        print(f"\nResult for {file_path}:\n{result}")
    elif mode == 'directory':
        directory = input("Enter the directory path: ")
        results = extract_text_from_directory(directory, txt_processing_dir=text_directory, ocr_mode=ocr_mode)
        for file, result in results.items():
            print(f"\n{file}:\n{result}")
    else:
        print("Invalid mode. Choose 'single' or 'directory'.")

# if __name__ == "__main__":
#     main()


# Test usage of the ollama library to generate a response using the DeepSeek-R1 model.
def test_ollama_generate():
    """Test Ollama generate function with DeepSeek-R1 model."""
    try:
        response = ollama.generate(
            model="deepseek-r1:8b",
            prompt="Write a Python function to calculate the factorial of a number."
        )
        print(response['response'])
    except Exception as e:
        print(f"Error generating response: {e}")

# Sample output:
'''
<think>
We are going to write a function that calculates the factorial of a non-negative integer...
'''
# test_ollama_generate()

# Test function
def test_embed_query():
    query = "What is the main topic of my documents?"
    embedding = embed_query(query)
    print(f"Query embedding length: {len(embedding)}")
    print(f"Sample embedding values: {embedding[:5]}")  # Print first 5 values for inspection
'''Expected type of output: 
Query embedding length: 384
Sample embedding values: [0.123456, -0.789012, 0.345678, -0.234567, 0.678901]'''

# test_embed_query()

def test_retrieve_chunks(vector_directory=vector_directory):
    query = "What is the main topic of my documents?"
    chunks = retrieve_chunks(query, vector_directory, k=3) # 3 chunks selected
    print(f"Retrieved {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}:")
        print(f"Source: {chunk['source']}")
        print(f"Text: {chunk['text'][:100]}...")
'''Expected type of output: (not relevant to the query)
Retrieved 3 chunks:
Chunk 1:
Source: doc1.txt
Text: This is the first 100 characters of the chunk from doc1...
Chunk 2:
Source: doc1.txt
Text: Another chunk from the same or different document...'''

# test_retrieve_chunks()

def test_assemble_context():
    length = 80
    mock_chunks = [
        {"text": "This is the first document chunk about AI.", "source": "doc1.txt"},
        {"text": "This is the second chunk discussing machine learning.", "source": "doc2.txt"}
    ]
    context = assemble_context(mock_chunks, max_context_length=length)
    print(f"Assembled context (truncated to {length} chars):\n{context}")
'''Expected type of output:
Assembled context (truncated to 80 chars):
This is the first document chunk about AI.

This is the second chunk discussing'''

# test_assemble_context()

def test_generate_response():
    query = "Show evidence of safety measures for Project X."
    context = """[Source: safety_report.txt] Project X uses certified materials meeting ISO 9001 standards.

[Source: training_log.txt] All personnel are trained per OSHA guidelines."""
    # Test without thinking
    print("Testing without thinking:")
    response = generate_response(query, context, show_thinking=False)
    print(f"Generated response:\n{response}\n")
    
    # Test with thinking
    print("Testing with thinking:")
    response = generate_response(query, context, show_thinking=True)
    print(f"Generated response:\n{response}")
'''Expected type of output:
Generated response:
Testing without thinking:
Here is the evidence...

Testing with thinking:
<think>
Okay, let me think through this...
'''
# test_generate_response()

top_k = 5
depth = 1
def test_rag_pipeline():
    query = "Show evidence of lessons learned from Bishopsgate project."
    vector_store_path = f"{directory}/{vector_directory}"
    print(f"Testing pipeline with top_k={top_k}, depth={depth}:")
    response = rag_pipeline(query, vector_store_path, k=top_k, depth=depth, show_thinking=False)
    print(f"RAG pipeline response:\n{response}\n")
    
    print(f"Testing pipeline with top_k={top_k}, depth=2:")
    response = rag_pipeline(query, vector_store_path, k=top_k, depth=2, show_thinking=True)
    print(f"RAG pipeline response:\n{response}")

# test_rag_pipeline()

