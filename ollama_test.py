import ollama
import os

import PyPDF2

response = ollama.generate(
    model="deepseek-r1:8b",
    prompt="Write a Python function to calculate the factorial of a number."
)
print(response['response'])

# print("Hello, World")

# # Function to read file content
# def read_file(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             return file.read()
#     except Exception as e:
#         return f"Error reading file: {str(e)}"

# # Function to process file with DeepSeek-R1
# def process_file(file_path, task="summarize"):
#     content = read_file(file_path)
#     if "Error" in content:
#         return content

#     # Define the prompt based on the task
#     if task == "summarize":
#         prompt = f"Summarize the following content in 100 words or less:\n\n{content}"
#     elif task == "extract":
#         prompt = f"Extract key information (e.g., names, dates, main topics) from:\n\n{content}"
#     else:
#         prompt = f"Process the following content: {task}\n\n{content}"

#     # Call DeepSeek-R1
#     try:
#         response = ollama.generate(
#             model="deepseek-r1:8b",
#             prompt=prompt
#         )
#         return response['response']
#     except Exception as e:
#         return f"Error processing with DeepSeek: {str(e)}"

# # Process files in a directory
# directory = "path/to/your/files"  # Replace with your directory path
# for filename in os.listdir(directory):
#     if filename.endswith(".txt"):  # Adjust for other file types as needed
#         file_path = os.path.join(directory, filename)
#         result = process_file(file_path, task="summarize")
#         print(f"File: {filename}\nResult: {result}\n")



# def read_pdf(file_path):
#     try:
#         with open(file_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             return " ".join(page.extract_text() for page in reader.pages)
#     except Exception as e:
#         return f"Error reading PDF: {str(e)}"