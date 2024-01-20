from sentence_transformers import SentenceTransformer
from typing import List
class TextVectorizer:
    """
    Class for vectorizing text using SentenceTransformer models.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the TextVectorizer object.

        Args:
            model_name (str): Name of the SentenceTransformer model to use.
        """
        self.model = SentenceTransformer(model_name)

    def read_articles(self, file_path: str) -> List[str]:
        """
        Read articles from a file and split them into chunks.

        Args:
            file_path (str): Path to the file containing the articles.

        Returns:
            List[str]: List of articles.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            articles = file.read().split('----')  # Разделение статей
        return articles

    def chunk_article(self, article: str, chunk_size: int = 500) -> List[str]:
        """
        Split an article into chunks of specified size.

        Args:
            article (str): The article to be chunked.
            chunk_size (int): Size of each chunk.

        Returns:
            List[str]: List of chunks.
        """
        words = article.split()
        chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        return chunks

    def get_all_chunks(self, articles: List[str]) -> List[str]:
        """
        Get all chunks from a list of articles.

        Args:
            articles (List[str]): List of articles.

        Returns:
            List[str]: List of all chunks.
        """
        all_chunks = []
        for article in articles:
            chunks = self.chunk_article(article)
            all_chunks.extend(chunks)
        return all_chunks

    def vectorize_chunks(self, chunks: List[str]) -> List[List[float]]:
        """
        Vectorize a list of chunks using the SentenceTransformer model.

        Args:
            chunks (List[str]): List of chunks.

        Returns:
            List[List[float]]: List of chunk embeddings.
        """
        embeddings = [self.model.encode(chunk) for chunk in chunks]
        return embeddings
