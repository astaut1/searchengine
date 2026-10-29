from fastapi import FastAPI, Request, Form,BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastpai import bm25_query
from dataloader import csv_data_loader
from utils import data_dictionary_from_content
from methods.bm25 import build_bm25_index, bm25_index_query_with_snippets
from crawl_utils import crawl


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mock database for search
data_path = "index_data.csv"
data = csv_data_loader(data_path)
content_data = data_dictionary_from_content(data)

def execute_crawl(url: str):
  print(f"Crawling started for: {url}...")
  success_status, error = crawl(url)  # Assuming your crawl function takes the URL

  if success_status:
    print("Site crawled successfully!")
  else:
    print(f"Site could not be crawled! Error: {error}")

def bm25_query(item: str)-> list[str]:
    tfidf_index = build_bm25_index(data)
    result = bm25_index_query_with_snippets(tfidf_index, item,content_data,20,200)
    return result

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "search.html", {"results": None, "query": ""})


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    # Run your search script logic here
    results = bm25_query(query)
    refined_results = []
    for result in results:
        title = data.loc[data['url'] == result['url'],'title'].item()
        print(title)
        if "—" in title:
            continue
        refined_results.append({
            "title": title,
            "url": result["url"],
            "score": result["score"],
            "snippets": result["snippets"]
        })

    return templates.TemplateResponse(request, "search.html", {"results": refined_results, "query": query})

@app.post("/crawl")
async def crawl_site(
    background_tasks: BackgroundTasks, crawl_url: str = Form(...)
):
  # Queue the crawl function to run in the background with the URL
  background_tasks.add_task(execute_crawl, crawl_url)

  # Immediately return a success response to the frontend JavaScript
  return JSONResponse({
      "status": "success",
      "message": (
          f"Background crawl initiated for {crawl_url}. Check terminal for"
          " progress!"
      ),
  })