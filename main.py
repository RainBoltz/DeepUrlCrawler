import requests
import pandas as pd
from lxml import html
from urllib.parse import urljoin

class DeepCrawler:
    def __init__(self, start_page):
        self.visited_url = {}
        self.queue_url = [start_page]


    def get_url_list(self, url):
        print('crawling: %s'%(url))
        
        try:
            response = requests.get(url, timeout=10.0)
            raw_html = response.text
            parsed_html = html.fromstring(raw_html)
        except:
            return
        
        url_title_item = parsed_html.xpath('//title')
        url_title = '(NO TITLE)'
        try:
            url_title = url_title_item[0].text
        except:
            url_title = '(ERROR TITLE)'
        self.visited_url[url] = url_title
    
        for a in parsed_html.xpath('//a'):
            raw_url = a.get('href')
            if raw_url is None:
                continue
            
            parsed_url = urljoin(url, raw_url)
            if parsed_url not in list(self.visited_url.keys()) and parsed_url not in self.queue_url:
                self.queue_url.append(parsed_url)
    
    def output_result(self):
        result = pd.DataFrame()
        urls = list(self.visited_url.keys())
        titles = list(self.visited_url.values())
        
        result['TITLE'] = titles
        result['URL'] = urls
        
        result.to_csv('result.csv', encoding='utf-8-sig')
        
    def start_crawling(self, threshold=-1):
        while threshold is not 0:
            this_url = self.queue_url[0]
            self.get_url_list(this_url)
            
            if len(self.queue_url) == 1:
                break
            else:
                self.queue_url = self.queue_url[1:]
                
            threshold -= 1
        
        self.output_result()
        print('DONE!')
        
        
        
myCrawler = DeepCrawler('https://github.com/rainboltz')
myCrawler.start_crawling(threshold=25)
        
        
        
        
        
        
        
        
                
            