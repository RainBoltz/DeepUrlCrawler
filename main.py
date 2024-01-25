from BSScraper import BSScraper
from embedder import Embedder

def Embed(document):
    embedder_module = Embedder()
    embedder_module.generate(document, "shah_rukh_khan")

if (__name__ == '__main__'):
    #bsScraper = BSScraper(threshold=10)
    #bsScraper.start_crawler('https://en.wikipedia.org/wiki/Shah_Rukh_Khan', Embed)

    em = Embedder()
    docs = em.search("shah_rukh_khan", "Which did shah rukh grow up?")

    