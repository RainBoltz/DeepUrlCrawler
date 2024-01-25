import requests
import pandas as pd
from lxml import html
from lxml.html.clean import Cleaner
from urllib.parse import urljoin
import re

class DeepCrawler:
    def __init__(self, start_page):
        self.visited_url = {}
        self.queue_url = [start_page]
        
        # html cleaner
        self.cleaner = Cleaner()
        self.cleaner.javascript = True
        self.cleaner.style = True
        self.cleaner.kill_tags = ['img']


    def get_url_list(self, url):
        print('crawling: %s'%(url))
        
        try:
            url = url.lower()
            response = requests.get(url, timeout=10.0)
            raw_html = response.text
            parsed_html = self.cleaner.clean_html(html.fromstring(raw_html))
            cleaned_html = html.tostring(parsed_html).decode("utf-8")
        except:
            print(f"ERROR while crawling")
            return
        
        url_title_item = parsed_html.xpath('//title')
        url_title = '(NO TITLE)'
        try:
            url_title = url_title_item[0].text
        except:
            url_title = '(ERROR TITLE)'
        self.visited_url[url] = url_title

        # spans, p etc
        html_text = cleaned_html
        TAG_RE = re.compile(r'<[^>]+>')
        LINE_RE = re.compile(r'\n+')
        TAB_RE = re.compile(r'\t+')
        stripped = TAG_RE.sub(' ', html_text)
        stripped = LINE_RE.sub(' ', stripped)
        stripped = TAB_RE.sub(' ', stripped)
    
        for a in parsed_html.xpath('//a'):
            raw_url = a.get('href')
            if raw_url is None:
                continue
            
            parsed_url = urljoin(url, raw_url)
            if parsed_url not in list(self.visited_url.keys()) and parsed_url not in self.queue_url:
                self.queue_url.append(parsed_url)

        return f"{stripped}"
    
    def output_result(self):
        result = pd.DataFrame()
        urls = list(self.visited_url.keys())
        titles = list(self.visited_url.values())
        
        result['TITLE'] = titles
        result['URL'] = urls
        
        result.to_csv('result.csv', encoding='utf-8-sig')
        
    def start_crawling(self, fn_callback, threshold=-1):
        while threshold > 0:
            this_url = self.queue_url[0]
            output = self.get_url_list(this_url)
            
            if (fn_callback is not None):
                fn_callback(output)

            if len(self.queue_url) == 1:
                break
            else:
                self.queue_url = self.queue_url[1:]
                
            threshold -= 1
        
        self.output_result()
        print('DONE!')
        
if (__name__ == '__main__'):
    myCrawler = DeepCrawler('https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html')
    myCrawler.start_crawling(lambda op: print(op), threshold=30)
        
        
        
        
        
        
        
        
                
            