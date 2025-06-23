# PROJECT HACK 25 - GROUP 1F 
## "The Winning Team"
18/06/2025

Project to build a local instance of a ~multimodal~ GenAI.
Model choice: ` deepseek-r1:8b `
Embedding model choice: ` all-MiniLM-L6-v2 `

# Git repo
https://github.com/Loxodromia/Local_LLM/

MVP branch - V1, single prompt on RAG with Streamlit UI, no parsing:  ` RAG ` https://github.com/Loxodromia/Local_LLM/tree/RAG

Most current branch - V3, structured data and iteration over list of queries from spreadsheet, designed to document evidence for a list of KSBs (Knowledge, Skills and Behaviours) for apprenticeship work: ` quote ` (built from ` struct-output `) https://github.com/Loxodromia/Local_LLM/tree/quote

## File Structure
* Files for RAG are placed in folder ` INPUT/ ` (excluded from git in .gitignore). The txt processing files will be created in a subfolder of the input directory, as well as the indexing.
* ` fileprocessing.py ` contains the readers and processors to turn multiple file types into text, then save in a subfolder.
* ` RAG.py ` contains the langchain functions to chunk and index these text files into a vector store for RAG.
* ` tests.py ` contains past tests during development in raw form, for future creation of automated tests.
* ` structure_output.py ` contains functions to parse the LLM response into structured fields (e.g. confidence %) and aggregate data for the csv output.


# Install
(In VSCode)

Install Ollama: `https://ollama.com/download`

Install `requirements.txt` which should include all the dependencies.
Run `ollama serve` to check it works. Leave that terminal open and open a new one.
Run `ollama run deepseek-r1:8b`
Write something to test the model and then `/exit`
Run the script.

# Dependencies

1. Install Tesseract for OCR: ` https://github.com/UB-Mannheim/tesseract/wiki `
Run the installer. By default, it installs to C:\Program Files\Tesseract-OCR. Otherwise, adjust the path in ` fileprocessing.py ` # Dependencies
Verify installation by opening a Command Prompt and running:

` tesseract --version `

You should see the Tesseract version (e.g., tesseract v5.3.4).

2. Install Poppler for pdf 2 image: ` https://stackoverflow.com/questions/53481088/poppler-in-path-for-pdf2image `
Meaning, download it and unzip in a location whose path you'll enter in ` fileprocessing.py ` # Dependencies


### Troubleshooting: 

1. <b> If ollama is not recognised in VSCode </b>
` ollama: command not found ` in VSCode
Check if Ollama is Installed:

Open a PowerShell or Command Prompt outside VSCode - e.g. cmd.exe - and run:
` ollama --version `
If it returns a version (e.g., ollama version is 0.3.12), Ollama is installed. If not, reinstall it.

Reinstall Ollama (if needed): Download the Ollama installer for Windows from https://ollama.com/download. 
Run the installer, ensuring you select the option to add Ollama to your system PATH (if prompted).
After installation, verify in PowerShell:
` ollama serve `
This should start the server without errors.

Add Ollama to Bash PATH (if you prefer Bash):
If you want to keep using Bash (e.g., Git Bash), add Ollama to its PATH:
Find Ollama’s executable path. On Windows, it’s typically in ` C:\Users\<YourUser>\AppData\Local\Programs\Ollama\ollama.exe `
Edit your Bash profile (e.g., ~/.bashrc or ~/.bash_profile):
` nano ~/.bashrc `

Add:
`export PATH="$PATH:/c/Users/<YourUser>/AppData/Local/Programs/Ollama" `
Replace <YourUser> with your Windows username (use forward slashes / for Bash).

Reload the profile:
`source ~/.bashrc `

Test in VSCode’s Bash terminal:
`ollama serve `

2. If there is a multiple usage error: `Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted`
* Close the Ollama window and if still happening, open the Task Manager and close any ollama processes. Then restart VSCode and try again.


