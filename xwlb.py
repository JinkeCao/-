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
from datetime import date, timedelta


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
        , timeout = 99
        ).read()
    return BeautifulSoup(
        res
        , features="lxml"
        )


b = date(
    2013
    , 12
    , 10
    )
e = date(
    2007
    , 1
    , 1
    )


while b >= e:
    try:
        xl = [
            x.get_text().strip()
            for x in link2bs(
                    'https://cn.govopendata.com/xinwenlianbo/'
                    + str(b).replace('-','')
                    +'/'
                    ).find(
                        class_='col-md-9 col-sm-12 heti'
                        ).find_all(
                            [
                                'a'
                                , 'p'
                                ]
                            )
            ]
        with open(
                'F:/Users/Administrator/Documents/2022认知组前瞻预研/xwlb/'
                + str(b).replace('-','')
                + '.json'
                , 'a'
                , encoding='utf8'
                ) as f:
            dump(
                [
                     {
                      'title': xl[i]
                      ,'text': xl[i+1]
                      } for i in range(
                          0
                          , len(xl)
                          , 2
                          )
                          ]
                          , fp = f
                          , ensure_ascii= False
                          , indent=True
                )
    finally: 
        b -= timedelta(
            days = 1
            )
        sleep(99)
        continue
