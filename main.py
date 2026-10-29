from ranked_inverted_index import *
from inverse_index import build_inverted_index, inverted_index_query
from tfidf import build_tfidf_index, tfidf_index_query,tfidf_index_query_with_snippets
from bm25 import build_bm25_index, bm25_index_query
from utils import *
from dataloader import *


csv_path = "index_data.csv"
query = "brownie"

def tftidx_with_snippets():
    print("Query Tokens:", tokenise(query))
    data = csv_data_loader(csv_path)
    content_data = data_dictionary_from_content(data)
    tfidf_index = build_tfidf_index(data)
    result = tfidf_index_query_with_snippets(tfidf_index, query, content_data)
    print(result)
    print(len(result))

def ranked_inverse_index_with_snippets():
    data = csv_data_loader(csv_path)
    ranked_index = build_ranked_inverted_index(data)
    content_data = data_dictionary_from_content(data)
    tfidf_index = build_tfidf_index(data)
    ranked_inverse_search = ranked_inverted_index_query_with_snippets(ranked_index,query,content_data)
    print(ranked_inverse_search)
    print(len(ranked_inverse_search))


def simple_tfidf():
    data = csv_data_loader(csv_path)
    tfidf_index = build_tfidf_index(data)
    result = tfidf_index_query(tfidf_index, query)
    print(result)
    print(len(result))

def inverted_index():
    data = csv_data_loader(csv_path)
    inverted_index = build_inverted_index(data)
    result, time_taken = measure_time(inverted_index_query,inverted_index,query)
    print("Time Taken:", time_taken)
    print("Result:", result)
    print(len(result))

def ranked_inverted_index():
    data = csv_data_loader(csv_path)
    ranked_index = build_ranked_inverted_index(data)
    result = ranked_inverted_index_query(ranked_index, query)
    print(result)
    print(len(result))

def bm25_query():
    data = csv_data_loader(csv_path)
    tfidf_index = build_bm25_index(data)
    result = bm25_index_query(tfidf_index, query)
    print(result)
    print(len(result))


def main():
    simple_tfidf()
    bm25_query()


if __name__ == "__main__":
    main()