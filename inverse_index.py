import pandas as pd
from utils import tokenise,measure_time
from dataloader import build_index_file, get_index_from_file
import os

inverse_index_file_path = "inverted_index.json"

def build_inverted_index(data:pd.DataFrame) -> dict[str,set[str]]:
    if os.path.exists(inverse_index_file_path):
        #as the file is saved as dict[str,list[str]], it needs to be converted into dict[str,set[str]]
        raw_data = get_index_from_file(inverse_index_file_path)
        inverted_index: dict[str, set[str]] = {key: set(value) for key, value in raw_data.items()}
    else:
        inverted_index = None

    if inverted_index is None:
        inverted_index = {}
        # each row in the db table has attributes url,title,date_retrieved,text
        # but the csv data loader omits the date_retrieved data
        # so each row in data.itertupes has row.url,row.title,row.text
        for row in data.itertuples():
            token_candidates = row.title # + " "+ row.text
            tokens = set(tokenise(token_candidates))
            for token in tokens:
                if token not in inverted_index:
                    inverted_index[token] = set()
                inverted_index[token].add(row.url)
        #as sets cannot be dumped into json, the sets are first converted to lists
        serializable_data = {key: list(value) for key, value in inverted_index.items()}
        build_index_file(serializable_data,inverse_index_file_path)

    return inverted_index


def inverted_index_query(inverted_index:dict[str,set[str]],query:str) ->list[str]:
    result_set = []
    tokens = set(tokenise(query))
    for token in tokens:
        url_set = inverted_index.get(token,set())
        result_set.append(url_set)
    result = list(set.union(*result_set))
    #prints the number of results per token
    for es in result_set:
        print(len(es))
    return result