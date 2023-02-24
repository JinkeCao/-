# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 17:37:45 2022

@author: ckcao
"""


# from kafka import KafkaProducer
from json import dump
from random import choice
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep#, mktime, strptime
# from uuid import uuid5, NAMESPACE_DNS
# from urllib.parse import urlencode
# import datetime
# from re import findall
# import ssl
from selenium import webdriver
from func_timeout import func_set_timeout, FunctionTimedOut

def genHeader():
    headerset = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70'
            }
        , {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            }
        , {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
            }
        ]
    return choice(headerset)

def link2bs(link):
    req = Request(
        link
        , headers=genHeader()
        )
    res = urlopen(
        req
        , timeout = 59
        ).read()
    return BeautifulSoup(
        res
        , features="lxml"
        )

@func_set_timeout(99)
def link2bso(link):
    driver = webdriver.Chrome(
        r'C:\Users\ckcao\Downloads\chromedriver.exe'
        )
    driver.implicitly_wait(59)
    try:
        driver.get(link)
        sleep(9)
        bso = BeautifulSoup(
            driver.page_source
            , features="lxml"
            )
        driver.quit()
        return bso
    except Exception as e:
        driver.quit()
        return BeautifulSoup(
            str(e)
            , features="lxml"
            )
        

def timered_link2bso(link):
    try: bso = link2bso(link)
    except FunctionTimedOut: bso = BeautifulSoup(
        'timesout'
        , features="lxml"
        )
    except Exception as e:
        bso = BeautifulSoup(
            str(e)
            , features="lxml"
            )
    return bso

def path_cleaner(path):
    for c in r'<>/\|:*? ': path = path.replace(c, '_')
    return path

slp = 9*4
for a in BeautifulSoup(
        open(
            r'F:\Users\Administrator\Documents\2022认知组前瞻预研\milifeng3-35200-\3-35200-.xml'
            , 'r'
            , encoding='utf8'
             ).read()
        ).find_all(
                'a'
                , class_='news-stream-newsStream-image-link'
                ):
    print(a['title'])
    sleep(slp)
    r = {}
    try:
        bs = link2bs(
            'https:'
            + a['href']
            )
        sleep(slp)
        r['title'] = a['title']
        r['source']=bs.find(
            class_='sourceTitleText-3cWSuiol'
            ).get_text()
        r['time'] = bs.find(
            class_='timeBref-2lHnksft'
            ).get_text()
        r['text'] = [
            p for p in bs.find(
                class_='main_content-r5RGqegj'
                ).stripped_strings
            ]
        try:
            bso = timered_link2bso(
                r'https://gentie.ifeng.com/c/comment/'
                + a['href'].split('/')[-1]
                ).find(
                    class_='comment_box-1dciHGm9'
                    ).find_all('div')
            sleep(slp)
            r['hot_comments'] = [
                {
                    'screen_name': c[0]
                    , 'reply': c[-14]
                    , 'recommendation': c[-12]
                    , 'disapproval': '0'
                    , 'reply_to_object':[]
                    }
                if len(c) <= 16
                else {
                    'screen_name': c[0]
                    , 'reply': c[-14]
                    , 'recommendation': c[-12]
                    , 'disapproval': '0'
                    , 'reply_to_object':[
                        {
                            'screen_name': c[c.index(x) - 1]
                            , 'comments': c[c.index(x) + 1]
                            , 'Recommendation': c[c.index(x) + 3]
                            , 'disapproval': '0'
                            }
                        for x in c
                        if '[' == x[0] and c.index(x) >= 4
                        ]
                    }
                for c in [
                    [
                        s for s in c.stripped_strings
                        ] for c in bso[0].find_all(
                            class_='comment_box-2hOInx9W'
                            )
                        ]
                ]
        except Exception as e:
            print(str(e))
            sleep(slp)
            r['hot_comments'] = [{}]
        with open(
                r'F:\Users\Administrator\Documents\2022认知组前瞻预研\milifeng3-35200-'
                + '//'
                + path_cleaner(
                    a['href'].split('/')[-1]
                    )
                + '_'
                + path_cleaner(
                    a['title']
                    )
                + '.json'
                , 'a'
                , encoding='utf8'
                ) as f:
            dump(
                r
                , fp = f
                , ensure_ascii= False
                , indent=True
                )
            print(
                ''
                ,file=f
                )
    except Exception as e:
        print(str(e))
        sleep(slp)
        continue
