import re

import pandas as pd
from inverse_index import build_inverted_index, inverted_index_query
from utils import *
from dataloader import *

csv_path = "index_data.csv"


def inverted_index_search(inverted_index:{},query: str) ->list[str]:
    print(query)




def main():
    query = "cake cakes "
    print("Search Results:", tokenise(query))
    data = csv_data_loader(csv_path)
    inverted_index = build_inverted_index(data)
    print('Lengh of Index', len(inverted_index))
    result, time_taken = measure_time(inverted_index_query,inverted_index,query)
    print("Time Taken:", time_taken)
    print("Result:", result)
    print(len(result))
    for s in result:
        print(len(s))
        print(s)



if __name__ == "__main__":
    main()