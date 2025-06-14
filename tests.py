
from ollama_fn import process_file
from fileprocessing import read_csv, read_pdf, read_image, read_doc, read_docx, read_odt, read_ppt, read_pptx, read_txt, read_xls, read_excel
from fileprocessing import extract_text_from_file, extract_text_from_directory
import os
import pytesseract

# Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
print(pytesseract.image_to_string(Image.open(f'{directory}sample.jpg')))

# Input
directory = "INPUT/"  # Replace with your directory path
text_directory = f"{directory}text_files"  # Directory for .txt files
vector_directory = f"{directory}vector_store"  # Directory for vector store

#----------------------------------
# CHECKS
#----------------------------------

# Embeddings model loading
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded successfully!")

# Single file samples by extension
print(read_pptx(f'{directory}guidance.pptx'))
print(read_excel(f'{directory}Reqs.xlsx'))
print(read_docx(f'{directory}RFP - SOR.docx'))
print(read_txt(f'{directory}tbc.txt'))
print(read_pdf(f'{directory}Sign-in & Set-up MFA.pdf'))

# General file reading
file_text = extract_text_from_file(f'{directory}guidance.pptx', ocr_mode=False, troubleshoot=True)
print(file_text)

# Process files in a directory
print(extract_text_from_directory(directory, ocr_mode=False, troubleshoot=True))

# Main function to process files
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

if __name__ == "__main__":
    main()