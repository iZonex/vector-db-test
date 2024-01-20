from typing import List
from .searcher import MilvusSearcher
from .vectorizer import TextVectorizer
from utils.data_reader import read_articles_from_folder


DATA_FOLDER = 'data'

def init_db(host: str = "localhost", port: str = "19530") -> None:
    """
    Main function that performs the vectorization, indexing, and searching of articles.
    """
    # Initialize TextVectorizer
    text_vectorizer = TextVectorizer()

    # Read and process all .txt files in the 'data' folder
    folder_path = DATA_FOLDER
    articles = read_articles_from_folder(folder_path)

    # Lists to store vectors and corresponding texts
    embeddings = []
    texts = []

    # Process each article
    for article in articles:
        chunks = text_vectorizer.get_all_chunks([article])
        for chunk in chunks:
            # Add the chunk text to the texts list
            texts.append(chunk)
            # Vectorize the chunk and add the result to the embeddings list
            embedding = text_vectorizer.vectorize_chunks([chunk])[0]
            embeddings.append(embedding)

    # Initialize MilvusSearcher
    searcher = MilvusSearcher(host, port)
    collection_name = 'article_collection'
    dim = 384  # Dimensionality of the model vectors

    # Create collection and index in Milvus
    collection = searcher.create_collection(collection_name, dim)
    searcher.create_index(collection)

    # Insert vectorized data and corresponding texts into the collection
    ids = searcher.insert_data(collection, embeddings, texts)
    collection.load()

    print(f"Inserted {len(ids)} vectors into collection {collection_name}.")
