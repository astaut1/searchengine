import math
import os
from math import floor

import pandas as pd
from utils import tokenise, measure_time, create_snippet,tokenise_with_stopwords
from dataloader import get_index_from_file,build_index_file

# Implementation of Best Matching 25
# Improved Version of TF-IDF
# It introduces Term Frequency Saturation and Document Length Normalisation
# TF = ( number of occurrences + k1 + 1 ) / (number of occurrences + k1 * ( 1 + b + b * (length of document / avg document length) ) )
# IDF = log ( 1 + (total number of documents in corpus - 0.5 / number of documents containing keyword - 0.5 ) )

bm_25_file_path = "../indexes/bm25_index.json"
ranked_index_file_path = "../indexes/ranked_inverted_index.json"

def calculate_idf(total_docs,frequency):
    if total_docs <= 0:
        return 0
    return math.log(((total_docs-frequency+0.5)/(frequency+0.5)) +1)

def build_bm25_index(data:pd.DataFrame, k1: float = 1.5, b: float = 0.5) -> dict[str,dict[str,float]]:
    if os.path.exists(bm_25_file_path):
        idf_index = get_index_from_file(bm_25_file_path)
        return idf_index

    if os.path.exists(ranked_index_file_path):
        ranked_inverted_index = get_index_from_file(ranked_index_file_path)
        idf_index = {}
        wordcount = {}
        total_wordcount = 0
        for row in data.itertuples():
            token_candidates = row.title + " " + row.text.lower()
            tokens = tokenise_with_stopwords(token_candidates)
            wordcount[row.url] = len(tokens)
            total_wordcount += len(tokens)

        total_docs = len(ranked_inverted_index) + 1
        avg_wordcount = total_wordcount / total_docs

        for token, document_count in ranked_inverted_index.items():
            idf = calculate_idf(total_docs, len(document_count))
            idf_index[token] = {}
            for url, count in document_count.items():
                length_normalizer = (1 - b + (b * (wordcount[url] / avg_wordcount)))
                term_frequency = (count+(k1+1)  )/ (count + k1* length_normalizer)
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

        total_docs = len(ranked_inverted_index) + 1
        for token,document_count in ranked_inverted_index.items():
            idf = calculate_idf(total_docs,len(document_count))
            idf_index[token] = {}
            for url,count in document_count.items():
                length_normalizer = (1 - b + (b * (wordcount[url] / avg_wordcount)))
                term_frequency = (count+(k1+1))/ (count + k1* length_normalizer)
                idf_index[token][url] = term_frequency * idf


    build_index_file(idf_index,bm_25_file_path)
    return idf_index

def bm25_index_query(bm25_index:dict[str,dict[str,float]],query: str) -> list[str]:
    results = []
    tokens = tokenise_with_stopwords(query)
    scores = {}
    for token in tokens:
        if token in bm25_index:
            print(token)
            url_set = bm25_index.get(token,{})
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

def bm25_index_query_with_snippets(bm25_index:dict[str,dict[str,float]],query: str,content_data: dict[str,str],number_of_results=3, snippet_length:int = 100) -> list[str]:
    final_results = []
    tokens = tokenise_with_stopwords(query)
    scores = {}
    for token in tokens:
        if token in bm25_index:
            print(token)
            url_set = bm25_index.get(token,{})
            for url, score in url_set.items():
                if url not in scores:
                    scores[url] = 0
                scores[url] += score

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    number_of_results = number_of_results if number_of_results < len(ranked) else len(ranked)
    for i in range(0,number_of_results):
        url, score = ranked[i]
        snippets = create_snippet(tokens, content_data[url],1,snippet_length)
        final_results.append({
            "url": url,
            "score": score,
            "snippets": snippets
        })

    return final_results

