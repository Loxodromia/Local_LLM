*This is VISION and though it was meant to destroy us all, it will end up saving us.*

Project to build a local instance of a ~multimodal~ GenAI.
Model choice: ` deepseek-r1:8b `

# Install
(In VSCode)

Install Ollama: `https://ollama.com/download`

Install `requirements.txt` which should include all the dependencies.
Run `ollama serve` to check it works. Leave that terminal open and open a new one.
Run `ollama run deepseek-r1:8b`
Write something to test the model and then `/exit`
Run the script.

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
Find Ollama’s executable path. On Windows, it’s typically in ` C:\Users\ <YourUser> \AppData\Local\Programs\Ollama\ollama.exe `
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

# Dependencies

1. Install Tesseract for OCR: ` https://github.com/UB-Mannheim/tesseract/wiki `
Run the installer. By default, it installs to C:\Program Files\Tesseract-OCR.

Add Tesseract to your system PATH:
Right-click "This PC" → Properties → Advanced system settings → Environment Variables.

Under "System variables," find Path, click Edit, and add C:\Program Files\Tesseract-OCR.

Verify installation by opening a Command Prompt and running:
` tesseract --version `

You should see the Tesseract version (e.g., tesseract v5.3.4).

2. Install Poppler for pdf 2 image: ` https://stackoverflow.com/questions/53481088/poppler-in-path-for-pdf2image `

