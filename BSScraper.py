from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class BSScraper:
    def __init__(self, threshold = 1):
        self.doc_queue = []
        self.visited_links = []
        self.threshold = threshold

    def start_crawler(self, url, callback_fn):
        self.doc_queue = [url]

        while (self.doc_queue.__len__() > 0 and self.threshold > 0):
            url = self.doc_queue[0]
            print(f"Reading URL: {url}\n")
            loader = AsyncChromiumLoader([url])
            html = loader.load()

            soup = BeautifulSoup(html[0].page_content, "html.parser")
            a_tags = soup.findAll('a', href=True)

            for a_tag in a_tags:
                link_path = a_tag['href']
                if (link_path is not None):
                    abs_url = None
                    if (link_path.startswith('/')):
                        rel_url = link_path
                        abs_url = urljoin(url, rel_url)
                    if (link_path.startswith('https://')):
                        abs_url = a_tag.href

                    if (abs_url is not None and abs_url not in list(self.visited_links) and abs_url not in list(self.doc_queue)):
                        self.doc_queue.append(abs_url)

            self.visited_links.append(url)
            self.doc_queue = self.doc_queue[1:]
            self.threshold -= 1

            bs_transformer = BeautifulSoupTransformer()
            docs_transformed = bs_transformer.transform_documents(
                html, tags_to_extract=["title", "p", "li", "div", "a", "span"]
            )

            if (callback_fn is not None and docs_transformed.__len__() > 0):
                callback_fn(docs_transformed[0].page_content)

if (__name__ == '__main__'):
    bsScraper = BSScraper(threshold=10)
    bsScraper.start_crawler('https://en.wikipedia.org/wiki/Shah_Rukh_Khan', lambda docs: print(f"Generated {docs.__len__()} documents"))