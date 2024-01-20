from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility,
)


class MilvusSearcher:
    def __init__(self, host: str = "localhost", port: str = "19530") -> None:
        """
        Initialize the MilvusSearcher class.

        Args:
            host (str): The host address of the Milvus server. Default is 'localhost'.
            port (str): The port number of the Milvus server. Default is '19530'.
        """
        connections.connect(host=host, port=port)

    def create_index(
        self,
        collection: Collection,
        index_type: str = "IVF_FLAT",
        metric_type: str = "L2",
        params: dict = {"nlist": 128},
    ) -> None:
        """
        Create an index for a collection.

        Args:
            collection (Collection): The collection to create the index for.
            index_type (str): The type of index to create. Default is "IVF_FLAT".
            metric_type (str): The type of metric to use for indexing. Default is "L2".
            params (dict): Additional parameters for the index. Default is {"nlist": 128}.
        """
        field_name = "embedding"
        index_params = {
            "index_type": index_type,
            "metric_type": metric_type,
            "params": params,
        }
        collection.create_index(field_name, index_params)

    def get_collection(self, collection_name: str) -> Collection:
        """
        Get a collection by name.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            Collection: The collection object.
        """
        return Collection(collection_name)

    def create_collection(self, collection_name: str, dim: int) -> Collection:
        """
        Create a new collection.

        Args:
            collection_name (str): The name of the collection.
            dim (int): The dimension of the embedding vectors.

        Returns:
            Collection: The created collection object.
        """
        if utility.has_collection(collection_name):
            Collection(collection_name).drop()

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=6000),
        ]

        schema = CollectionSchema(fields, description="Text Embedding Collection")

        collection = Collection(name=collection_name, schema=schema)

        return collection

    def insert_data(
        self, collection: Collection, embeddings: list, texts: list
    ) -> list:
        """
        Insert data into a collection.

        Args:
            collection (Collection): The collection to insert data into.
            embeddings (list): List of embedding vectors.
            texts (list): List of corresponding texts.

        Returns:
            list: List of primary keys of the inserted data.
        """
        mr = collection.insert([embeddings, texts])
        collection.load()
        return mr.primary_keys

    def search_vectors(
        self, collection: Collection, query_vector: list, top_k: int
    ) -> list:
        """
        Search for vectors in a collection.

        Args:
            collection (Collection): The collection to search in.
            query_vector (list): The query vector.
            top_k (int): The number of nearest neighbors to retrieve.

        Returns:
            list: List of search results.
        """
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        return collection.search(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["text"],
        )

    def combined_search(
        self,
        collection: Collection,
        query_text: str,
        query_vector: list,
        top_k: int = 10,
    ) -> list:
        """
        Perform a combined search using both text and vector queries.

        Args:
            collection (Collection): The collection to search in.
            query_text (str): The text query.
            query_vector (list): The vector query.
            top_k (int): The number of results to retrieve. Default is 10.

        Returns:
            list: List of filtered and ranked search results.
        """
        result = self.search_vectors(collection, query_vector, top_k)
        filtered_and_ranked_results = []
        for hits in result:
            for hit in hits:
                text = hit.entity.get("text")
                if query_text.lower() in text.lower():
                    filtered_and_ranked_results.append(
                        (hit.id, hit.distance, hit.entity.get("text"))
                    )

        filtered_and_ranked_results.sort(key=lambda x: x[1])

        return filtered_and_ranked_results
