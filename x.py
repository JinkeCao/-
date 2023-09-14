#from hashlib import md5
from bs4 import BeautifulSoup
from json import dump
from time import sleep
#from urllib.request import Request, urlopen
#from random import choice
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from func_timeout import func_set_timeout, FunctionTimedOut
from os.path import abspath, join
from datetime import date
from os import makedirs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@func_set_timeout(99)
def link2bso(link):
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    o = webdriver.ChromeOptions()
    o.add_argument("--ignore-certificate-error")
    o.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(
        r'C:\Users\ckcao\Downloads\chromedriver-win32\chromedriver.exe'
        , desired_capabilities=capa
        , options = o
    )
    try:
        driver.get(
            link
            )
        sleep(22)
        driver.execute_script(
            "window.stop();"
            )
        driver.find_element(
            By.TAG_NAME,
            'body'
        ).send_keys(
            Keys.PAGE_DOWN
        )
        sleep(11)
        bso = BeautifulSoup(
            driver.page_source
            , features="lxml"
            )
        # driver.quit()
        # return bso
    except Exception as e:
        # driver.quit()
        bso = BeautifulSoup(
            str(
                e
                )
            , features="lxml"
            )
    finally:
        driver.quit()
        return bso
    
def timered_link2bso(link):
    try: bso = link2bso(link)
    except FunctionTimedOut: bso = 'TimedOut 99 secs'
    except Exception as e:
        print(str(e))
        bso = str(e)
    return bso

def te(
    x,
    l
):
    try:
        return l(
            x
        )
    except:
        return ''
def rclb(
        b
):
    try:
        return [t for t in b.select(
                '#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-jxzhtn.r-1ljd8xs.r-13l2t4g.r-1phboty.r-16y2uox.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div:nth-child(3) > div.css-1dbjc4n.r-18u37iz.r-1w6e6rj'
        )[0].stripped_strings]
    except:
        return ['']

for q in (
'LeungBaggio',
'chenqiushi404',
'realyuantengfei',
'RealGaoxiaosong',
'ZXZ3677',
'haohaidong1964',
'dayangelcp',
'fangshimin',
'YongyuanCui1',
'PanshiyiSOHO',
'imRZQ',
'liuxia64',
'shizuki_lena',
'Xuxiaodong3',
'MaoYuShi',
'0xCrocodile',
'ChipTsao817',
'samngx',
'comma_channel',
'proletariathk',
'hkStephenSYY',
'hkpeanuts',
'Tuesdayroad1',
'joshuawongcf',
'Ray_WongHKI',
'hoccgoomusic',
'PerryChsu',
'Andychanhotin',
'TonyChungHonLam',
'ClaudiaMCMo',
'degewa33',
'CardJosephZen',
'yauwaiching',
'nathanlawkc',
'ChuHoiDick',
'chowtingagnes',
'SunnyCheungky',
'SimonChengUK',
'honcqueslaus',
'samuelmchu',
'alexandroslee',
'romiansaran'
):
    try:
        for i in [
            y.find(
                'a',
                href = True
            )[
                'href'
            ] for y in timered_link2bso(
                'https://www.google.com/search?' + urlencode(
                    {
                        'q':'site:twitter.com ' + q,
                        'num': 10
                    }
                )
            ).find_all(
                class_='MjjYud'
            ) if 'status' in y.find(
                'a',
                href = True
            )[
                'href'
            ] and 'mobile' not in y.find(
                'a',
                href = True
            )[
                'href'
            ]
        ]:
            try:
                b = timered_link2bso(i)
                j = join(
                    abspath(
                        'F:/Users/Administrator/Documents/20230817_googletwitter'
                    ),
                    str(
                        date.today()
                    )
                ),
                j = j[0]
                makedirs(
                    j,
                    exist_ok=True
                )

                with open(
                    j
                    +'\\'
                    +q
                    +'_'
                    +i.split('/')[5].split('?')[0]
                    +'.json',
                    'w',
                    encoding='utf8'
                ) as f:
                    dump(
                        {
                            'account_url':te(
                                i,
                                lambda x: x.split(
                                    '/status/'
                                )[
                                    0
                                ]
                            ),
                            'account_id':te(
                                b,
                                lambda x:x.find(
                                    'div',
                                    class_="css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2"
                                ).get_text()
                            ),
                            'nick_name':te(
                                b,
                                lambda x:x.find(
                                    'div',
                                    attrs={
                                        'class':"css-901oao r-1awozwy r-18jsvk2 r-6koalj r-1qd0xha r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0",
                                        'dir':"ltr"
                                    }
                                ).get_text()
                            ),
                            'account_description':te(
                                b,
                                lambda x:x.find(
                                    'div',
                                    attrs={
                                        'class':"css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-1h8ys4a r-1jeg54m r-qvutc0",
                                        'dir':"auto"
                                    }
                                ).get_text()
                            ),
                            'post_url':i,
                            'post_id':te(
                                i,
                                lambda x:i.split(
                                    '/'
                                )[5].split(
                                    '?'
                                )[0]
                            ),
                            'content':te(
                                b,
                                lambda x:x.find(
                                    'title',
                                ).get_text()
                            ),
                            'pubtime':te(
                                b,
                                lambda x:x.find(
                                    'time'
                                ).attrs[
                                    'datetime'
                                ]
                            ),
                            'repost_comment_like_bookmark':rclb(
                                b
                            )
                        }
                        , fp = f
                        , ensure_ascii= False
                        , indent=True
                    )
            except Exception as e:
                print(
                    e.__traceback__.tb_frame.f_globals['__file__'],
                    e.__traceback__.tb_lineno,
                    e
                )
            finally:
                sleep(180)
                continue
    except Exception as e:
        print(
            e.__traceback__.tb_frame.f_globals['__file__'],
            e.__traceback__.tb_lineno,
            e
        )
    finally:
        sleep(180)
        continue
