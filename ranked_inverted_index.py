import pandas as pd
from utils import tokenise,measure_time

def build_ranked_inverted_index(data:pd.DataFrame) -> dict[str,dict[str,int]]:
    ranked_inverted_index = {}
    for row in data.itertuples():
        token_candidates = row.title #+ " " + row.text.lower()
        tokens = tokenise(token_candidates)
        for token in tokens:
            if token not in ranked_inverted_index:
                ranked_inverted_index[token] = {}
            if row.url not in ranked_inverted_index[token]:
                ranked_inverted_index[token][row.url]=1
            else:
                ranked_inverted_index[token][row.url] += 1
    return ranked_inverted_index

def ranked_inverted_index_query(ranked_inverted_index:dict[str,dict[str,int]],query:str) ->list[str]:
    result_set = []
    tokens = tokenise(query)
    scores : dict[str,int]=  {}
    for token in tokens:
        url_set = ranked_inverted_index.get(token,{})
        for url,count in url_set.items():
            if url not in scores:
                scores[url] = 0
            scores[url] += count
    ranked = sorted(
        scores.items(),
        key= lambda x: x[1],
        reverse=True
    )

    return [docs for docs, scores in ranked]

