import re
import time

import pandas as pd


def tokenise(query: str) ->list[str]:
    return re.findall(r"[a-zA-Z]+", query.lower())

def measure_time(func,*args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result,end-start

def data_dictionary_from_content(data:pd.DataFrame) -> dict[str,str]:
    # result_dict = {}
    # for row in data.itertuples():
    #     cleaned_text = row.text.replace('\r', ' ').replace('\n', ' ')
    #     result_dict[row.url] = cleaned_text

    #"faster for large datasets"
    result_dict = (data.set_index('url')['text']
                   .str.replace('\r', ' ', regex=False)
                   .str.replace('\n', ' ',regex=False)
                   .str.replace(r'\s+', ' ', regex=True)
                   .str.strip()
                   .to_dict())

    return result_dict



def create_snippet(query_items: list[str],content:str,max_snippets = 3,snippet_window=100) -> list[str]:
    content = content.lower()
    snippets = []
    start_pos = 0
    for item in query_items:
        position = content.find(item,start_pos)
        if position == -1:
            break
        snippet_start = max(0, position- snippet_window //2)
        snippet_end = min( position + snippet_window //2, len(content))
        snippet = content[snippet_start:snippet_end]
        snippet.replace("\n", ' ')
        snippets.append(snippet)
        start_pos = position + len(item)

    return snippets[:max_snippets]