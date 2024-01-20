import os
import wikipediaapi
import argparse

class WikipediaArticleFetcher:
    def __init__(self, data_dir='data', user_agent='MyUserAgent/1.0'):
        self.wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def fetch_article(self, title):
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

    def fetch_articles(self, titles):
        for title in titles:
            print(f"Fetching '{title}'...")
            self.fetch_article(title)
            print(f"Finished fetching '{title}'")

def main():
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
