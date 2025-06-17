import pandas as pd
import re
import numpy as np
import openpyxl

questions_file = r"INPUT/PEAT_reduced.xlsm"
sheet = r"2.1 LOEs, Artefacts & Assurance"
prompt_column = 6 # Line of Enquiry 1
startrow = 0  # Excel row number to start reading (1-indexed, so 11 means row 10 in 0-indexed Python)
headerrow = 20  # Excel row number to use as headers (1-indexed, so 10 means row 9 in 0-indexed Python)

def parse_llm_output_to_df(query, raw_output: str) -> pd.DataFrame:
    """
    Parse raw LLM output into a DataFrame with Answer, Confidence, and Source columns.
    
    Args:
        raw_output (str): The raw response from the LLM.
        
    Returns:
        pd.DataFrame: DataFrame with columns:
            - Answer: Full response text
            - Confidence: Highest confidence percentage as float (or NaN if none)
            - Source: Comma-separated string of file names from [Source: ...] tags
    """
    # Store the full response as the Answer
    answer = raw_output.strip()
    
    # Extract confidence percentages (with or without brackets)
    confidence_pattern = r"(?:\[Confidence: |Confidence: )(\d+)%\]"
    confidence_matches = re.findall(confidence_pattern, raw_output)
    highest_confidence = float(max([int(match) for match in confidence_matches])) if confidence_matches else np.nan
    
    # Extract file names from [Source: <a href="...">filename</a>] tags
    source_pattern = r"\[Source: <a href=\"[^\"]+\"[^>]*>([^<]+)</a>\]"
    source_matches = re.findall(source_pattern, raw_output)
    source_text = ", ".join(source_matches) if source_matches else ""
    
    # Create DataFrame with one row
    df = pd.DataFrame({
        "Question": [query],
        "Answer": [answer],
        "Confidence": [highest_confidence],
        "Source": [source_text]
    })
    
    return df

# Read prompt file
def read_xlsm_file(file_path: str, sheet_name: str = "Sheet1") -> pd.DataFrame:
    """
    Read an entire .xlsm file into a pandas DataFrame.
    
    Args:
        file_path (str): Path to the .xlsm file.
        sheet_name (str): Name of the sheet (default: "Sheet1").
        
    Returns:
        pd.DataFrame: DataFrame containing all data from the sheet.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the sheet is not found.
    """
    try:
        # Read the entire sheet from the .xlsm file
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
        
        # Debugging: Print basic info about the loaded data
        # print(f"Loaded {len(df)} rows and {len(df.columns)} columns from '{file_path}', sheet '{sheet_name}'")
        # print(f"Columns: {list(df.columns)}")
        # print(df.head())
        
        # Keep only first N columns (A to AA, 0-indexed: 0 to 26)
        df_a = df.iloc[:, :9]  # Keep first N columns
        # Drop first 2 columns (0-indexed, so 2 means drop first 2 columns)
        df_a = df_a.iloc[:, 2:]  # Drop first 2 columns (

        # Drop first x rows (0-indexed, so 10 means drop first 10 rows)
        df_a = df_a.iloc[7:]  # Drop first 10 rows (0

        # Drop rows where prompt column is NaN or empty
        df_b = df_a.dropna(subset=[df.columns[5]])  
        
        # set first row as header, dropping it afterwards
        df_b.columns = df_b.iloc[0]  # Set first row as header
        df_b = df_b[1:]  # Drop the first row after setting it as header

        # Rename "Line of Enquiry (Level 1)" column to "Prompt"
        df_b.rename(columns={df_b.columns[4]: "Prompt"}, inplace=True)

        print(df_b.head())  # Debugging: Print first few rows of the cleaned DataFrame

        return df_b
    
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' was not found.")
    except ValueError as e:
        if "No sheet" in str(e):
            raise ValueError(f"Sheet '{sheet_name}' not found in the file '{file_path}'.")
        raise e
    
read_xlsm_file(questions_file, sheet).head()
