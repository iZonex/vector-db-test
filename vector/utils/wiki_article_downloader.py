import os
import wikipediaapi
import argparse

class WikipediaArticleFetcher:
    def __init__(self, data_dir: str = 'data', user_agent: str = 'MyUserAgent/1.0'):
        """
        Initializes the WikipediaArticleFetcher class.

        Args:
            data_dir (str): The directory to store the downloaded articles.
            user_agent (str): The user agent string to use for making requests to Wikipedia.
        """
        self.wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def fetch_article(self, title: str) -> str:
        """
        Fetches the content of a Wikipedia article.

        Args:
            title (str): The title of the article.

        Returns:
            str: The content of the article.
        """
        data_path = os.path.join(self.data_dir, f"{title}.txt")
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as file:
                return file.read()

        page = self.wiki_wiki.page(title)
        if page.exists():
            with open(data_path, 'w', encoding='utf-8') as file:
                file.write(page.text)
            return page.text
        else:
            print(f"Article '{title}' does not exist.")
        return None

    def fetch_articles(self, titles: list[str]) -> None:
        """
        Fetches multiple Wikipedia articles.

        Args:
            titles (list[str]): The titles of the articles to fetch.
        """
        for title in titles:
            print(f"Fetching '{title}'...")
            self.fetch_article(title)
            print(f"Finished fetching '{title}'")

def main() -> None:
    """
    The main function that is executed when the script is run.
    """
    parser = argparse.ArgumentParser(description="Fetch Wikipedia Articles")
    parser.add_argument('titles', nargs='*', default=[
        "Economic growth", "New York City", "Artificial intelligence",
        "Machine learning", "Python (programming language)", "Data science",
        "Data mining", "Data visualization", "Data structure", "Data analysis"
    ], help="Titles of Wikipedia articles to fetch")
    args = parser.parse_args()

    fetcher = WikipediaArticleFetcher()
    fetcher.fetch_articles(args.titles)

if __name__ == "__main__":
    main()
