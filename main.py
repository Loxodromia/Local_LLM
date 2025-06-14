from ollama_fn import process_file
from fileprocessing import read_csv, read_pdf, read_image, read_doc, read_docx, read_odt, read_ppt, read_pptx, read_txt, read_xls, read_excel
from fileprocessing import chunk_content, extract_text_from_file, extract_text_from_directory
import os
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# from PIL import Image

# Input
directory = "INPUT/"  # Replace with your directory path

# Process files in a directory
# for filename in os.listdir(directory):
#     if filename.endswith(".txt"):  # Adjust for other file types as needed
#         file_path = os.path.join(directory, filename)
#         result = process_file(file_path, task="summarize")
#         print(f"File: {filename}\nResult: {result}\n")



# print(pytesseract.image_to_string(Image.open(f'{directory}sample.jpg')))

# Single file samples
# print(read_pptx(f'{directory}guidance.pptx'))
# print(read_excel(f'{directory}Reqs.xlsx'))
# print(read_docx(f'{directory}RFP - SOR.docx'))
# print(read_txt(f'{directory}tbc.txt'))
# print(read_pdf(f'{directory}Sign-in & Set-up MFA.pdf'))

print(extract_text_from_file(f'{directory}Sign-in & Set-up MFA.pdf', ocr_mode=False, troubleshoot=False))
