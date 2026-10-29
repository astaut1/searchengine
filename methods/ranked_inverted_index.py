import os

import pandas as pd
from utils import tokenise, measure_time, create_snippet,tokenise_with_stopwords
from dataloader import get_index_from_file,build_index_file

ranked_index_file_path = "../indexes/ranked_inverted_index.json"

def build_ranked_inverted_index(data:pd.DataFrame) -> dict[str,dict[str,int]]:
    if os.path.exists(ranked_index_file_path):

        ranked_inverted_index = get_index_from_file(ranked_index_file_path)
    else:
        ranked_inverted_index = None

    if ranked_inverted_index is None:
        ranked_inverted_index = {}
        for row in data.itertuples():
            token_candidates = row.title + " " + row.text.lower()
            tokens = tokenise_with_stopwords(token_candidates)
            for token in tokens:
                if token not in ranked_inverted_index:
                    ranked_inverted_index[token] = {}
                if row.url not in ranked_inverted_index[token]:
                    ranked_inverted_index[token][row.url]=1
                else:
                    ranked_inverted_index[token][row.url] += 1
        build_index_file(ranked_inverted_index,ranked_index_file_path)
    return ranked_inverted_index

def ranked_inverted_index_query(ranked_inverted_index:dict[str,dict[str,int]],query:str) ->list[str]:
    result_set = []
    tokens = tokenise_with_stopwords(query)
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


def ranked_inverted_index_query_with_snippets(ranked_inverted_index:dict[str,dict[str,int]],query:str,content_data: dict[str,str],number_of_results=3) ->list[str]:
    result_set = []
    tokens = tokenise_with_stopwords(query)
    scores : dict[str,int]=  {}
    final_results = []
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

    for i in range(0,number_of_results):
        url,score = ranked[i]
        snippets = create_snippet(tokens,content_data[url])
        final_results.append({
            "url":url,
            "score":score,
            "snippets":snippets
        })



    return final_results
