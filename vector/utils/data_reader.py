import os
from typing import List


def read_articles_from_folder(folder_path: str) -> List[str]:
    """
    Read and return the contents of all .txt files in the specified folder.

    Args:
        folder_path: The path to the folder containing the .txt files.

    Returns:
        A list of strings, where each string represents the content of a .txt file.
    """
    all_articles = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                article = file.read()
                all_articles.append(article)
    return all_articles