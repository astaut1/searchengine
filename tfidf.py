import math
import os
import pandas as pd
from utils import tokenise, measure_time, create_snippet,tokenise_with_stopwords
from dataloader import get_index_from_file,build_index_file

tf_idf_file_path= "tfidf.csv"
ranked_index_file_path = "ranked_inverted_index.json"

def build_tfidf_index(data:pd.DataFrame) -> dict[str,dict[str,float]]:
    if os.path.exists(tf_idf_file_path):
        idf_index = get_index_from_file(tf_idf_file_path)
        return idf_index

    if os.path.exists(ranked_index_file_path):
        ranked_inverted_index = get_index_from_file(ranked_index_file_path)
        idf_index = {}
        wordcount = {}
        for row in data.itertuples():
            token_candidates = row.title + " " + row.text.lower()
            tokens = tokenise_with_stopwords(token_candidates)
            wordcount[row.url] = len(tokens)
        total_docs = len(ranked_inverted_index)

        for token, document_count in ranked_inverted_index.items():
            idf = calculate_idf(total_docs, len(document_count))
            idf_index[token] = {}
            for url, count in document_count.items():
                term_frequency = count / wordcount[url]
                idf_index[token][url] = term_frequency * idf

    else:
        ranked_inverted_index = None

    if ranked_inverted_index is None:
        ranked_inverted_index = {}
        idf_index={}
        wordcount = {}
        for row in data.itertuples():
            token_candidates = row.title + " " + row.text.lower()
            tokens = tokenise_with_stopwords(token_candidates)
            wordcount[row.url] = len(tokens)
            for token in tokens:
                if token not in ranked_inverted_index:
                    ranked_inverted_index[token] = {}
                if row.url not in ranked_inverted_index[token]:
                    ranked_inverted_index[token][row.url]=1
                else:
                    ranked_inverted_index[token][row.url] += 1
        build_index_file(ranked_inverted_index,ranked_index_file_path)

        total_docs = len(ranked_inverted_index)
        for token,document_count in ranked_inverted_index.items():
            idf = calculate_idf(total_docs,len(document_count))
            idf_index[token] = {}
            for url,count in document_count.items():
                term_frequency = count / wordcount[url]
                idf_index[token][url] = term_frequency * idf

    build_index_file(idf_index,tf_idf_file_path)
    return idf_index


def calculate_idf(total_docs,frequency):
    print("doc type:",type(total_docs))
    print("freq type",type(frequency))
    if total_docs <= 0:
        return 0
    return math.log((total_docs+1)/(frequency+1))


def tfidf_index_query(tfidf_index:dict[str,dict[str,float]],query: str) -> list[str]:
    results = []
    tokens = tokenise_with_stopwords(query)
    scores = {}
    for token in tokens:
        if token in tfidf_index:
            print(token)
            url_set = tfidf_index.get(token,{})
            for url, score in url_set.items():
                if url not in scores:
                    scores[url] = 0
                scores[url] += score

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return [docs for docs, scores in ranked]

def tfidf_index_query_with_snippets(tfidf_index:dict[str,dict[str,float]],query: str,content_data: dict[str,str],number_of_results=3) -> list[str]:
    final_results = []
    tokens = tokenise_with_stopwords(query)
    scores = {}
    for token in tokens:
        if token in tfidf_index:
            print(token)
            url_set = tfidf_index.get(token,{})
            for url, score in url_set.items():
                if url not in scores:
                    scores[url] = 0
                scores[url] += score

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    for i in range(0,number_of_results):
        url, score = ranked[i]
        snippets = create_snippet(tokens, content_data[url])
        final_results.append({
            "url": url,
            "score": score,
            "snippets": snippets
        })

    return final_results