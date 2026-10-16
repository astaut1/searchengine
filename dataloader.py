import pandas as pd
import numpy as np
import sqlite3

def data_loader(database_path: str) -> pd.DataFrame:
        with sqlite3.connect(database_path) as conn:
            df = pd.read_sql_query("SELECT * FROM crawldata", conn)
        data = df.loc[:,'url','title','text']
        return data


def csv_data_loader(csv_path: str)-> pd.DataFrame:
    data = pd.read_csv(csv_path)
    return data
