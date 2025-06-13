from ollama_fn import process_file
import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

from PIL import Image

# Input
directory = "INPUT/"  # Replace with your directory path

# Process files in a directory
# for filename in os.listdir(directory):
#     if filename.endswith(".txt"):  # Adjust for other file types as needed
#         file_path = os.path.join(directory, filename)
#         result = process_file(file_path, task="summarize")
#         print(f"File: {filename}\nResult: {result}\n")



print(pytesseract.image_to_string(Image.open(f'{directory}sample.jpg')))