import pandas as pd
from utils import tokenise,measure_time

def build_inverted_index(data:pd.DataFrame) -> dict[str,list[str]]:
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

    return inverted_index


def inverted_index_query(inverted_index:dict[str,list[str]],query:str) ->list[str]:
    result_set = []
    tokens = tokenise(query)
    for token in tokens:
        url_set = inverted_index.get(token,set())
        result_set.append(url_set)
    result = list(set.union(*result_set))
    print('len of result set',len(result_set))
    return result