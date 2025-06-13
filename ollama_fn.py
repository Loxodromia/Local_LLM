
import ollama

# Function to process file with DeepSeek-R1
def process_file(file_path, task="summarize"):
    content = read_file(file_path)
    if "Error" in content:
        return content

    # Define the prompt based on the task
    if task == "summarize":
        prompt = f"Summarize the following content in 100 words or less:\n\n{content}"
    elif task == "extract":
        prompt = f"Extract key information (e.g., names, dates, main topics) from:\n\n{content}"
    else:
        prompt = f"Process the following content: {task}\n\n{content}"

    # Call DeepSeek-R1
    try:
        response = ollama.generate(
            model="deepseek-r1:8b",
            prompt=prompt
        )
        return response['response']
    except Exception as e:
        return f"Error processing with DeepSeek: {str(e)}"
