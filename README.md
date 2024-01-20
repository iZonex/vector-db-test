# Vector


<img width="851" alt="Screenshot 2024-01-20 at 02 25 04" src="https://github.com/iZonex/vector-db-test/assets/2759749/fb01ca8a-be78-4f54-8ab5-d6d9a561ef70">


Vector is an API server built using FastAPI. It utilizes Milvus as its database and leverages a suite of open-source libraries and modules for its operation. The server primarily handles vector-based data querying and ranking using text matches, offering distance metrics for the matches found. It includes an integrated web form for queries, which interacts with the graph database and processes vector data.

## Dependencies

Vector is developed with Python 3.11 and uses several open-source libraries, including:

- `Wikipedia-API==0.6.0`
- `transformers==4.36.2`
- `torch==2.1.2`
- `nltk==3.8.1`
- `pymilvus==2.3.5`
- `sentence-transformers==2.2.2`
- `fastapi==0.109.0`
- `uvicorn==0.26.0`

These dependencies are essential for the proper functioning of Vector and must be installed for the application to run correctly.

## Installation

To install and run Vector, follow these steps:

**Clone the Repository:**

   git clone <https://github.com/iZonex/vector-db-test.git>
   cd vector-db-test

**Build and Run with Docker:**

Ensure Docker and Docker Compose are installed on your system. Then, execute the following command in the project directory:

    docker-compose up --build

This command will build the Docker image and start the necessary services.

**Access the Application:**

Once the application is running, it will be accessible via <http://127.0.0.1:8000>, <http://0.0.0.0:8000>, or <http://localhost:8000>, depending on your system's configuration and Docker settings.

Please note that the initial setup and loading of the application can take approximately 2-3 minutes, depending on your system. This duration is necessary for the initialization of the database and the fetching of updates.

## Usage

Once Vector is up and running, you can use the web form provided on the application's main page to make queries. The application processes these queries by:

Accessing the graph database.
Working with vector data.
Ranking the results based on text matches.
Providing a distance metric for each match.
For data loading, Vector uses the Wikipedia-API module to fetch articles, which are then processed and stored in the Milvus database for querying.

## Attention

Code didn't covered Fuzzy Search from Levenshtein or Jaro-Winkler.
