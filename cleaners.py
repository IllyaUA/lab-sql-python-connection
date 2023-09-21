import pandas as pd
import difflib

def drop_null_by_column(df: pd.DataFrame, col_names: list) -> pd.DataFrame:
    # Check if col_names is a list
    if not isinstance(col_names, list):
        raise ValueError("col_names should be a list of column names.")

    # Drop null values for each column in col_names
    for col_name in col_names:
        if col_name not in df.columns:
            print(f"Warning: Column '{col_name}' not found in the DataFrame.")
        else:
            df.dropna(subset=[col_name], inplace=True)

    return df

def cols_names(df: pd.DataFrame, col_name_old: str, col_name_new: str) -> pd.DataFrame:
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')  # Rename + standardize column names
    df.rename(columns={col_name_old: col_name_new}, inplace=True)
    return df

def genders(df:pd.DataFrame)->pd.DataFrame:
    # Rename values in the "Geneder" column
    df["gender"] = df["gender"].replace({"[Ff]": "F"}, regex=True)
    df["gender"] = df["gender"].replace({"[Mm]": "M"}, regex=True) #! Order is imoprtant, sinve Female containe 'm', thus [Ff] - first!
    df['gender'].fillna('D', inplace=True) #Gender - replace with "D"
    return df
   
# Function to standardize values in a column
def standardize_column_values(df, mappings):
    for col, mapping in mappings.items():
        if col in df.columns:
            df[col] = df[col].replace(mapping, regex=True)
    return df

# df_fixed = standardize_dataframe_columns(df, mappings)

# Function to find the closest match in the state_mapping dictionary
def find_closest_match(mapping: dict, real_name: str, threshold: float) -> str:
    best_match = None
    best_ratio = threshold  # Set an initial value based on the threshold
    
    for state, abbreviation in mapping.items():
        ratio = difflib.SequenceMatcher(None, real_name, state).ratio()
        if ratio >= threshold and ratio >= best_ratio:
            best_match = abbreviation
            best_ratio = ratio
    
    if best_match:
        return best_match
    return real_name

def fix_abbreviations(df: pd.DataFrame, mapping: dict, col_name: str, threshold: float) -> pd.DataFrame:
    # Use the apply method to replace values in the specified column
    # Pass the threshold parameter explicitly to find_closest_match
    df[col_name] = df[col_name].apply(lambda x: find_closest_match(mapping, x, threshold))
    return df

#def cleaner(df:pd.DataFrame)
#   df=df.copy()
#   df = df.reset_index(drop = True)
   
 