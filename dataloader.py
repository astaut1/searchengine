import pandas as pd
import numpy as np
import sqlite3

def data_loader(database_path: str):
        with sqlite3.connect(database_path) as conn:
            df = pd.read_sql_query("SELECT * FROM crawldata", conn)
        data = df.loc[:,'url','title','text']
        return data
