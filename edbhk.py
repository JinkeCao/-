# -*- coding: utf-8 -*-
"""

@author: jkcao
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
import ssl
from selenium import webdriver
from func_timeout import func_set_timeout, FunctionTimedOut
from selenium.webdriver.common.keys import Keys
from pandas import read_html, ExcelWriter

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
    return BeautifulSoup(
        res
        , features="lxml"
        )

@func_set_timeout(199)
def link2bso(link):
    # driver = webdriver.Chrome(r'F:\Users\Administrator\Downloads\chromedriver.exe')
    driver = webdriver.Chrome(r'D:\Users\jkcao\Downloads\chromedriver_107\chromedriver.exe')
    driver.implicitly_wait(33)
    try:
        driver.get(link)
        c = 0
        sleep(9)
        while True:
            # height = driver.execute_script(r'return  document.documentElement.scrollTop || window.pageYoffset || document.body.srcollTop')
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            sleep(1)
            # next_height = driver.execute_script(r'return  document.documentElement.scrollTop || window.pageYoffset || document.body.srcollTop')
            c += 1
            if c > 5: break
            # elif height == next_height: break
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

s = set()
with open(
        r'F:\Users\Administrator\Documents\Python Scripts\temp.txt'
        , encoding='utf8'
        ) as f:
    for l in f:
        if 'schoolinfo' in l:
            s.add(l.strip().strip('&type='))
for i in s:
    # sleep(19)
    try:
        df = read_html(
            'https://applications.edb.gov.hk/schoolsearch/'
            # 'schoolinfo.aspx?langno=2&scrn=564311000111'
            + i
            # , header = None
            # , index_col = None
            )
        with ExcelWriter(
                r'F:\xmfr\edbhk'
                + '\\'
                + str(i.split('scrn=')[1])
                + '_'
                + str(df[0][1][1])
                + '.xlsx'
                # , mode = 'a'
                ) as f:
            df[0].to_excel(
                f
                , sheet_name = '學校資料'
                , header = False
                , index = False
                )
            df[1].to_excel(
                f
                , sheet_name = '註冊資料'
                , header = False
                , index = False
                )
        sleep(30)
    except Exception as e:
        print(str(e))
        sleep(60)
        continue
