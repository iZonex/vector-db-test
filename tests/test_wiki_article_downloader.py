import unittest
from wiki_article_downloader import WikipediaArticleFetcher

class TestWikipediaArticleFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = WikipediaArticleFetcher()

    def test_fetch_article_existing(self):
        title = 'Python (programming language)'
        article = self.fetcher.fetch_article(title)
        self.assertIsNotNone(article)

    def test_fetch_article_non_existing(self):
        title = 'Non-existing article'
        article = self.fetcher.fetch_article(title)
        self.assertIsNone(article)

    def test_chunk_text(self):
        text = 'This is a sentence. This is another sentence.'
        chunks = self.fetcher.chunk_text(text)
        self.assertEqual(chunks, ['This is a sentence', 'This is another sentence'])

if __name__ == '__main__':
    unittest.main()