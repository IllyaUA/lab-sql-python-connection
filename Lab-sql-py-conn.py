import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine, MetaData

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.metrics import classification_report, f1_score, cohen_kappa_score

import getpass  # To get the password without showing the input

password = getpass.getpass()

#1 Establich conn 2 Sakila

connection_string = 'mysql+pymysql://root:'+password+'@localhost/sakila'
engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(bind=engine)

table_names = metadata.tables.keys()


#2. Write function rentals_month
def rentals_month(engine, month:int, year:int)->pd.DataFrame:
    query = f"""SELECT rental_id, rental_date, inventory_id, customer_id, return_date FROM rental
    WHERE EXTRACT(YEAR FROM rental_date) = {year} AND EXTRACT(MONTH FROM rental_date) = {month};
    """   
    try:
        # Execute the SQL query and fetch the data into a Pandas DataFrame
        rental_data = pd.read_sql_query(query, engine)
        return rental_data
    except Exception as e:
        print(f"An error occurred: {e}")

#3 rental_count_month

def rental_count_month(engine, month:int, year:int)->pd.DataFrame:
       # Group the filtered data by 'customer_id' and count the rentals
    return rentals_month(engine, month, year).groupby('customer_id').size().reset_index(name=f'rentals_{month}_{year}')

rdf1=rental_count_month(engine,5,2005)
rdf2=rental_count_month(engine,7,2005)
rdf2.head()

#4 Create a Python function called compare_rentals

def compare_rentals(rentals_df1, rentals_df2):
    # Merge the DataFrames on 'customer_id'
    merged_df = pd.merge(rentals_df1, rentals_df2, on='customer_id', how='inner')

    # Find columns with names containing "rentals_"
    month_columns = [col for col in merged_df.columns if "rentals_" in col]

    # Calculate the difference for each common column
    merged_df[f'difference_rentals'] = merged_df[month_columns[1]] - merged_df[month_columns[0]]

    return merged_df


# Example usage
compared_result = compare_rentals(rdf1, rdf2)
print(compared_result)