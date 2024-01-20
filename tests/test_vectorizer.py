import pytest
from vectorizer import TextVectorizer

class TestTextVectorizer:
    def setup_class(cls):
        cls.vectorizer = TextVectorizer()

    def test_read_articles(self):
        file_path = '/path/to/articles.txt'
        articles = self.vectorizer.read_articles(file_path)
        assert isinstance(articles, list)
        assert len(articles) > 0

    def test_chunk_article(self):
        article = 'This is a sample article.'
        chunks = self.vectorizer.chunk_article(article, chunk_size=5)
        assert isinstance(chunks, list)
        assert len(chunks) > 0

    def test_get_all_chunks(self):
        articles = ['Article 1', 'Article 2', 'Article 3']
        all_chunks = self.vectorizer.get_all_chunks(articles)
        assert isinstance(all_chunks, list)
        assert len(all_chunks) > 0

    def test_vectorize_chunks(self):
        chunks = ['Chunk 1', 'Chunk 2', 'Chunk 3']
        embeddings = self.vectorizer.vectorize_chunks(chunks)
        assert isinstance(embeddings, list)
        assert len(embeddings) > 0
        assert isinstance(embeddings[0], list)
        assert len(embeddings[0]) > 0