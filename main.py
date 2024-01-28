from BSScraper import BSScraper
from embedder import Embedder
from search import Search

def Embed(document):
    embedder_module = Embedder()
    embedder_module.generate(document, "iqvia")

if (__name__ == '__main__'):
    bsScraper = BSScraper(threshold=50)
    bsScraper.start_crawler('https://www.iqvia.com/', Embed)
    print('Embedding complete!')

    # search = Search("iqvia")
    # response = search.LLMChat("List some of Shah rukh khan's movies?")

    # print(response)

