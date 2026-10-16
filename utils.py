import re
import time

def tokenise(query: str) ->list[str]:
    return re.findall(r"[a-zA-Z]+", query.lower())

def measure_time(func,*args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result,end-start