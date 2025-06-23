import pandas as pd
import re
import numpy as np
import openpyxl

questions_file = r"INPUT/PEAT_reduced.xlsm"
sheet = r"2.1 LOEs, Artefacts & Assurance"
startrow = 7  # Excel row number to start reading (1-indexed, so 11 means row 10 in 0-indexed Python)

def parse_llm_output_to_df(query, raw_output: str) -> pd.DataFrame:
    """
    Parse raw LLM output into a DataFrame with Answer, Confidence, and Quote columns.
    
    Args:
        raw_output (str): The raw response from the LLM.
        
    Returns:
        pd.DataFrame: DataFrame with columns:
            - Answer: Full response text
            - Confidence: Highest confidence percentage as float (or NaN if none)
            - Quote: Original text from which the answer was derived
    """
    # Store the full response as the Answer
    answer = raw_output.strip()
    
    # Extract confidence percentages (with or without brackets)
    # Mapping for textual confidence levels
    confidence_map = {
        "High": 80,
        "Medium": 50,
        "Low": 10
    }

    # Regex pattern to match both percentage and text-based confidence
    pattern = r"(?:\[?Confidence: ?)(\d+|High|Medium|Low)%?\]?"

    # Find all matches
    matches = re.findall(pattern, raw_output, flags=re.IGNORECASE)

    # Convert matches to numeric values
    confidence_values = []
    for match in matches:
        if match.isdigit():
            confidence_values.append(float(match))
        else:
            confidence_values.append(confidence_map.get(match.lower(), np.nan))

    # Extract the source text by finding the quote between "Quote:" and the end of the response
    quote_pattern = r"Quote:\s*(.*?)(?=\n|$)"
    source_match = re.search(quote_pattern, raw_output, flags=re.IGNORECASE)
    source_text = source_match.group(1).strip() if source_match else "No quote found"
    source_text = source_text.replace('"', '')  # Remove any quotes from the source text
    source_text = source_text.replace("'", "")  # Remove any single quotes from the source text
    source_text = source_text.replace("`", "")  # Remove any backticks from the source text

    # Get the highest confidence
    highest_confidence = float(max(confidence_values)) if confidence_values else np.nan
    
    # Create DataFrame with one row
    df = pd.DataFrame({
        "Question": [query],
        "Answer": [answer],
        "Confidence": [highest_confidence],
        "Quote": [source_text]
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
        df_a = df_a.iloc[:, 2:]  # Drop first 2 columns 

        # Drop first x rows 
        df_a = df_a.iloc[startrow:]  # Drop first N rows

        # Drop rows where prompt column is NaN or empty
        df_b = df_a.dropna(subset=[df.columns[5]])  
        
        # set first row as header, dropping it afterwards
        df_b.columns = df_b.iloc[0]  # Set first row as header
        df_b = df_b[1:]  # Drop the first row after setting it as header

        # Rename "Line of Enquiry (Level 2)" column to "Prompt"
        df_b.rename(columns={df_b.columns[5]: "Prompt"}, inplace=True)

        print(df_b.head())  # Debugging: Print first few rows of the cleaned DataFrame

        return df_b
    
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' was not found.")
    except ValueError as e:
        if "No sheet" in str(e):
            raise ValueError(f"Sheet '{sheet_name}' not found in the file '{file_path}'.")
        raise e
    
# read_xlsm_file(questions_file, sheet).head()

# Read xlsx KSB file
def read_xlsx_file(file_path: str, sheet_name: str = "Sheet1") -> pd.DataFrame:
    """
    Read an entire .xlsx file into a pandas DataFrame.

    Args:
        file_path (str): Path to the .xlsx file.
        sheet_name (str): Name of the sheet (default: "Sheet1").

    Returns:
        pd.DataFrame: DataFrame containing all data from the sheet.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the sheet is not found.
    """
    try:
        # Read the entire sheet from the .xlsx file
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

        # Debugging: Print basic info about the loaded data
        # print(f"Loaded {len(df)} rows and {len(df.columns)} columns from '{file_path}', sheet '{sheet_name}'")
        # print(f"Columns: {list(df.columns)}")
        # print(df.head())

        # Keep only relevant columns
        columns_to_keep = [
            "Standard", "Pass", "Distinction", "Project", "Target date", "Type", "Queries"
        ]
        
        df = df[columns_to_keep]
        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' was not found.")
    except ValueError as e:
        if "No sheet" in str(e):
            raise ValueError(f"Sheet '{sheet_name}' not found in the file '{file_path}'.")
        raise e
    
# Process the KSB dataframe
def process_ksb_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the KSB DataFrame to clean and format it, iterating the distinction criteria, adding KSB context, etc.

    Args:
        df (pd.DataFrame): The KSB DataFrame.

    Returns:
        pd.DataFrame: Processed DataFrame with all KSBs including distinctions and pass.
    """
    # Ensure the DataFrame has the expected columns
    expected_columns = ["Standard", "Pass", "Distinction", "Project", "Target date", "Type", "Queries"]
    if not all(col in df.columns for col in expected_columns):
        raise ValueError(f"DataFrame must contain the following columns: {expected_columns}")
    
    # Replace Knowledge, Skills, and Behaviours with relevant prompt tips
    df["Type"] = df["Type"].replace({
        "Knowledge": "Knowledge: show understanding of concepts, theories, and principles.",
        "Skills": "Skill: demonstrate practical abilities and techniques.",
        "Behaviours": "Behaviour: demonstrate attitudes, values, and professional conduct."
    }, inplace=True)

    # Create a new row for each KSB with distinction criteria, merging all prompts into criteria column and adding the queries and type
    processed_rows = []
    for _, row in df.iterrows():
        # Add the standard KSB row
        processed_rows.append({
            "Standard": row["Standard"],
            "Criteria": f"Use file {row['Project']}.pdf to document evidence on {row['Standard']}: {row['Pass']}. {row['Queries']}. {row['Type']}",
            "Project": row["Project"],
            "Target date": row["Target date"]
        })

        # Add distinction criteria rows if they exist
        if pd.notna(row["Distinction"]):
            processed_rows.append({
                "Standard": row["Standard"],
                "Criteria": f"Use file {row['Project']}.pdf to document evidence on: {row['Standard']}(Distinction): {row['Distinction']}. {row['Queries']}. {row['Type']}",
                "Project": row["Project"],
                "Target date": row["Target date"]
            })

    # Create a new DataFrame from the processed rows
    processed_df = pd.DataFrame(processed_rows)

    return processed_df
