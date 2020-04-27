# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:09:10 2020
"""
import requests
import time
import random
import datetime

class AbsHtmlPage:
    timestamp = 0
    """
    param: url_sub 
    return: 取得した HTML テキスト
    """
    def getHtmlPage(self, url_sub):
        url_base = 'https://www.showroom-live.com'
        params = ''
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
            }
        
        # アクセス間隔を開けるための遅延処理
        randValue = random.uniform(1.0,1.9)
        print(randValue, url_base + url_sub)
        time.sleep(randValue)
        
        response = requests.get(url=url_base + url_sub, params=params, headers=headers)
        html = response.text
        return html
    
    def func1(self):
        return 'aaabbb'

# if __name__ == "__main__":
        