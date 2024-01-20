import pytest
from searcher import MilvusSearcher
from milvus import Collection

class TestMilvusSearcher:
    @pytest.fixture
    def searcher(self):
        return MilvusSearcher()

    def test_create_index(self, searcher):
        collection = Collection("test_collection")
        searcher.create_index(collection)
        # Assert that the index is created successfully
        assert collection.has_index()

    def test_get_collection(self, searcher):
        collection_name = "test_collection"
        collection = searcher.get_collection(collection_name)
        # Assert that the returned collection has the correct name
        assert collection.name == collection_name

    def test_create_collection(self, searcher):
        collection_name = "test_collection"
        dim = 128
        collection = searcher.create_collection(collection_name, dim)
        # Assert that the created collection has the correct name and dimension
        assert collection.name == collection_name
        assert collection.schema.fields[1].dim == dim

    def test_insert_data(self, searcher):
        collection = Collection("test_collection")
        embeddings = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        texts = ["text1", "text2"]
        primary_keys = searcher.insert_data(collection, embeddings, texts)
        # Assert that the data is inserted successfully and primary keys are returned
        assert len(primary_keys) == len(embeddings)

    def test_search_vectors(self, searcher):
        collection = Collection("test_collection")
        query_vector = [1.0, 2.0, 3.0]
        top_k = 5
        results = searcher.search_vectors(collection, query_vector, top_k)
        # Assert that the correct number of search results are returned
        assert len(results) == top_k

    def test_combined_search(self, searcher):
        collection = Collection("test_collection")
        query_text = "query"
        query_vector = [1.0, 2.0, 3.0]
        top_k = 10
        results = searcher.combined_search(collection, query_text, query_vector, top_k)
        # Assert that the correct number of filtered and ranked search results are returned
        assert len(results) <= top_k