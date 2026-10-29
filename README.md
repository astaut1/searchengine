# Information Retrieval Search Engine 🔍

A Python-based search engine implementation featuring classic and advanced text retrieval models from scratch. This project demonstrates how modern search engines process corpora, build indexes, and score documents using statistical ranking algorithms.

## 🚀 Features

* **Inverted Index:** Fast posting-list mapping of terms to document IDs for Boolean retrieval.
* **Ranked Inverted Index:** Frequency-aware index mapping terms to document IDs and term frequencies.
* **TF-IDF (Term Frequency-Inverse Document Frequency):** Vector space model scoring matching query terms against document importance while penalizing globally common words.
* **BM25 (Best Matching 25):** State-of-the-art probabilistic ranking function featuring term frequency saturation and document length normalization.

## Setup
1. Clone the repository (replace with your actual repository URL)

git clone https://github.com/astaut1/searchengine.gitgit

cd your-search-engine-repo

touch links.txt

 2. Create and activate a Python virtual environment (recommended)

python -m venv venv

 On Windows:
venv\Scripts\activate

 On macOS/Linux:
source venv/bin/activate

 3. Install the project in editable mode along with any dependencies defined in pyproject.toml

pip install -r requirements.txt

4. Run the project with:

uvicorn main:app --reload   

This project uses functions and the dataset from webcrawling project [https://github.com/astaut1/WebCrawler.git]
