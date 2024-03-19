import os, json
import requests, urllib
from typing import Union, List, Dict
from newspaper import Article
from newspaper import Config as nsConfig
from langchain.schema.document import Document 

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

nsconfig = nsConfig()
nsconfig.request_timeout = 10
## available customsearch engines
# e05ed9c7f48a0493a => climate_thematic
# 62633c193a02f46ed => whole web search
# 97bc39b705c784980 => indonesian news websites
engine_list = {
            "whole_web":"62633c193a02f46ed",
            "climate":"e05ed9c7f48a0493a",
            "indo_news":"97bc39b705c784980",
            "workforce":"5788b81475cf24f5a"
        }

class gsearch:
    def __init__(self, engine_type:str='whole_web'):
        """
        engine_type: any of "whole_web", "climate", or "indo_news"
        """
        self.url = "https://www.googleapis.com/customsearch/v1"
        self.engine = engine_list[engine_type]
    
    def search(
            self, 
            query:str, 
            n_results:int=5, 
            start_date:str=None, 
            end_date:str=None
        ):
        date_filter = ''
        if start_date is not None:
            date_filter += f' after:{start_date}'
        if end_date is not None:
            date_filter += f' before:{end_date}'

        results = []
        n_pages = n_results // 10 + 1
        for i in range(n_pages):
            start_num = (i*10) + 1
            start = str(start_num)
            q_url = urllib.parse.quote_plus('{} {}'.format(query, date_filter))
            target_url = f'{self.url}?key={GOOGLE_API_KEY}&cx={self.engine}&q={q_url}&start={start}'

            result = requests.get(target_url)
            if result.status_code == 400:
                print(query, ' ', start)
                break
            try:
                for idx, item in enumerate(result.json()['items']):
                    if idx < n_results:
                        data = {
                            "title":item['title'],
                            "url":item["link"],
                            "rank":start_num+idx,
                            "search_params":{
                                "search_term":query,
                                "query_date_range":{
                                    "start_date":start_date,
                                    "end_date":end_date
                                },
                            }
                        }
                        try:
                            data['snippet'] = item['snippet']
                        except:
                            print(query, ' ', start_num+idx, ' no snippet')
                        
                        results.append(data)
            except KeyError:
                print(query, ' ', start, ' no more results')
        return results
    
    def read_articles_as_dict(
            self, 
            search_res:List[Dict], 
            language:str='id', 
            to_summarize:bool=False, 
            get_keyterm:bool=False
        ) -> List[Dict]:
        news_details = []
        for res in search_res:
            
            article = Article(res['url'], language=language)
            try:
                article.download()
                article.parse()
                d = {
                    "source":res['url'],
                    "text":article.text,
                    "title":res['title']
                }
                if to_summarize or get_keyterm:
                    article.nlp()

                    if to_summarize:
                        d['summary'] = article.summary
                    if get_keyterm:
                        d['keyterm'] = article.keywords
            except Exception as e:
                print('Article {} cannot be processed. '.format(res['url']), e)
                continue
            
            news_details.append(d)

        return news_details
    
    def read_articles(
            self, 
            search_res:List[Dict], 
            language:str='id', 
            to_summarize:bool=False, 
            get_keyterm:bool=False
        ) -> List[Document]:
        news_details = []
        for res in search_res:
            article = Article(res['url'], language=language)
            try:
                article.download()
                article.parse()
                meta = {"source": res['url'], "title":res['title']}

                if to_summarize or get_keyterm:
                    article.nlp()
                    if get_keyterm:
                        meta['keyterm'] = article.keywords
                    if to_summarize:
                        meta['summary'] = article.summary

                doc =  Document(page_content=article.text, metadata=meta)
            except Exception as e:
                print('Article {} cannot be processed. '.format(res['url']), e)
                continue
            news_details.append(doc)

        return news_details
    
