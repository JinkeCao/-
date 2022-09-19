# -*- coding: utf-8 -*-
"""
本代码每1小时查询1次陕师大贴吧
@author: jkcao
"""

from kafka import KafkaProducer
from json import dumps
from random import choice
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep, mktime, strptime
from uuid import uuid5, NAMESPACE_DNS
from urllib.parse import urlencode
import datetime
from re import findall
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

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
    sleep(33)
    bs64_str = ''.join(
        findall(
            '<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;">[.\n\S\s]*?</code>'
            , str(
                res
                , 'utf-8'
                )
            )
        ).replace(
            '<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;"><!--'
            ,''
            ).replace(
                '--></code>'
                ,''
                )
    return BeautifulSoup(
        bs64_str
        , features="lxml"
            )
        

['3', '萌新求问，大学如何实现排便自由', '青山镇小...', '18:38', '卡卡罗特', '19:09']
['74', '我只能说：输', 'PuddinJ0ker', '9-5', 'rt', '沿溪大瀑...', '19:08']
[]
['8', '吧u助力我九级', 'c', '霸王', '16:32', '刚刚去校园超市买草稿纸，到柜台时收银员指着草稿纸问了句“一本吗？” 好巧不巧她刚好指着草稿纸上的“陕西师范大学”，而且由于平时高强度冲浪，我第一时间没意识到她是在问我是不是只买一本草稿本而不是问学校是不是一本，脱口就是一声“不，是大专。” 我这句话一出口，收银员、跟我同行的舍友都绷不住了，我也意识到了这一点，整的我也有点尴尬，三秒过后收银员才说“我是问你是不是只买一本。”我才给钱走人。 直到现在我舍友', 'HAMLET', '18:52']
while True:
    try:
        bs = link2bs(
            'https://tieba.baidu.com/f?'
            + urlencode(
                {
                    'kw': '陕西师范大学'
                    , 'ie': 'utf-8'
                    # , 'fr': 'search'
                    }
                )
            )
        for li in bs.find_all('li'):
            try:
                ss = [s for s in li.stripped_strings]
                # if ':' in ss[-1]:
                infoTitle = ss[1]
                infoAuthor = ss[-2]
                publishTime = int(
                    round(
                        mktime(
                            strptime(
                                datetime.datetime.now().strftime(
                                    "%Y-%m-%d "
                                    )
                                + ss[-1]
                                , '%Y-%m-%d %H:%M'
                                )
                            )
                        )
                    )
                content = ' '.join(ss)
                bizId = uuid5(NAMESPACE_DNS, content).hex[:8]
                d = {
                   	  "bizId": bizId,
                   	  "processName": 'yq-1.0.0',
                   	  "infoType": 1,
                   	  "infoSource": '陕西师范大学百度贴吧',
                   	  "infoTitle": infoTitle,
                   	  "infoAuthor": infoAuthor,
                   	  "publishTime": publishTime,
                   	  "content":content,
                   	  "sex":2
                }
                print(d)
                producer = KafkaProducer(
                    bootstrap_servers= '192.168.5.150:9092'
                    , value_serializer= lambda v: dumps(
                        v
                        ).encode(
                            'utf-8'
                            )
                    )
                producer.send(
                    'mq-yq-input-handle'
                    , d
                    )
                producer.close()
                sleep(9)
            except:
                sleep(9)
                continue
    except:
        sleep(9)
        continue
    sleep(3600)
