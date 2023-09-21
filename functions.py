
import pandas as pd

def delete_unamed_column(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes a Pandas DataFrame as input, and creates an internal copy.
    Then on the interal copy it checks wheter or not contains a column named "Unnamed: 0".
    If it exists, deletes the column and returns the modified DataFrame, otherwise returns
    the original DataFrame.

    Inputs:
    df: Pandas DataFrame

    Output:
    Modified Pandas DataFrame
    '''

    df2 = df.copy()

    if "Unnamed: 0" in df2.columns:
        df2 = df2.drop("Unnamed: 0", axis=1)

    return df2

def replace_missing_values(df: pd.DataFrame, options: dict={"column_name": "state"}) -> pd.DataFrame:
    '''
    This function picks a Pandas DataFrame and replaces the missing values of "column_name" with the most frequent
    value of the colum

    Inputs:
    df: Pandas DataFrame
    column_name: string

    Outputs:
    A Pandas DataFrame with the missing values of column "column_name" replaced.
    '''

    df2 = df.copy()

    if options is not None:
        # We compute the most frequent value of column "column_name"
        most_frequent_value = df2[options['column_name']].mode()[0]

        df2[options['column_name']] = df2[options['column_name']].fillna(most_frequent_value)

    return df2

def clean_gender_column(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function will take a Pandas DataFrame as an input and it will replace the values in
    the "gender" column ins such a way that any gender which is not Male or Female with be 
    replaced by "U" otherwise the genders will be either "F" or "M"

    Inputs:
    df: Pandas DataFrame

    Outputs:
    A pandas DataFrame with the values in the "gender" column cleaned.
    '''

    df2 = df.copy()

    if "gender" not in df2.columns:
        return df2
    else:
        #df2['gender'] = df2['gender'].apply(lambda x: x[0].upper() if x[0].upper() in ['M', 'F'] else "U")
        df2['gender'] = list(map(lambda x: x[0].upper() if x[0].upper() in ['M', 'F'] else "U", df2['gender']))
        return df2

def clean_dataframe(df: pd.DataFrame, options: dict={"column_name": "state"}) -> pd.DataFrame:
    '''
    This function will take a Pandas DataFrame and it will apply the previous functions in the library
    to clean some columns of the dataframe

    Inputs: 
    df: Pandas DataFrame

    Outputs:
    Another DataFrame
    '''

    df2 = df.copy()

    df2 = delete_unamed_column(df2)
    df2 = replace_missing_values(df2, options=options)
    df2 = clean_gender_column(df2)

    return df2
