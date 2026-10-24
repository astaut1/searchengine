import pandas as pd
import numpy as np
import sqlite3
import os
import json

# to add text to search, you need to uncomment in the build_index functions in inverse_index and ranked_inverted_index

def data_loader(database_path: str) -> pd.DataFrame:
        with sqlite3.connect(database_path) as conn:
            df = pd.read_sql_query("SELECT * FROM crawldata", conn)
        data = df.loc[:,'url','title','text']
        return data



def csv_data_loader(csv_path: str)-> pd.DataFrame:
    data = pd.read_csv(csv_path)
    return data

def get_index_from_file(file_path: str) -> pd.DataFrame:
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    return None

def build_index_file(data:dict[str,dict[str,int]],file_path:str) -> bool:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data,f)
        return True
    except Exception as e:
        print("Error in build_index_file:",e)
        return False