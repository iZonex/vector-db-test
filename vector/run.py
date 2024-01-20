import os

import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from core.data_processing import init_db
from core.searcher import MilvusSearcher
from core.vectorizer import TextVectorizer

MILVUS_HOST = os.environ.get('MILVUS_HOST', "0.0.0.0")  
MILVUS_PORT = os.environ.get('MILVUS_PORT', "19530")

init_db(MILVUS_HOST, MILVUS_PORT)
app = FastAPI()

# Инициализация TextVectorizer и MilvusSearcher
text_vectorizer = TextVectorizer()
searcher = MilvusSearcher(MILVUS_HOST, MILVUS_PORT)
collection = searcher.get_collection('article_collection')

# Модель для запроса поиска
class SearchRequest(BaseModel):
    query: str

# Настройка пути к статическим файлам
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    print("State information: Reading index")
    return FileResponse('static/index.html')

@app.post("/v1/search/")
async def search(request: SearchRequest):
    print(f"State information: Performing search for query '{request.query}'")
    query_vector = text_vectorizer.vectorize_chunks([request.query])[0]
    search_results = searcher.combined_search(collection, request.query, query_vector)

    if not search_results:
        raise HTTPException(status_code=404, detail="No results found")

    return {"version": "1.0", "query": request.query, "results": search_results}

if __name__ == "__main__":
    print("State information: Starting the server")
    uvicorn.run(app, host="0.0.0.0", port=8000)