# -*- coding: utf-8 -*-

chrome_driver='/iflytek/data/xa1dx/chromedriver-linux64/chromedriver'
chrome_browser='/iflytek/data/xa1dx/chrome-linux64/chrome'
minio_conf = {
    'endpoint': 'localhost:9000',
    'access_key': 'minio',
    'secret_key': '',
    'secure': False
}
minio_bucket='test0304'
kafka_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'group0304',
    'auto.offset.reset': 'earliest'
}
kafka_producer={
    'bootstrap.servers': 'localhost:9092'
}
kafka_input_topic='test0304'
kafka_output_topic='test0305'

from bs4 import BeautifulSoup
from json import loads, dumps
from time import sleep, time
from urllib.request import urlopen
from requests import get
from selenium import webdriver
from socket import gethostbyname
import re
from minio import Minio
from io import BytesIO
from confluent_kafka import Consumer,Producer
from selenium.webdriver.chrome.service import Service

def um(
    b,
    d,
):
    client = Minio(
        **minio_conf
    )
    client.put_object(
        bucket_name=minio_bucket,
        object_name=d,
        data=BytesIO(b),
        length=len(
            b
        )
    )
    return '{}/{}/{}'.format(
        minio_conf[
            'endpoint'
        ],
        minio_bucket,
        d
    )

def lh(
    link, 
    d
):
    o = webdriver.ChromeOptions()
    o.binary_location=chrome_browser
    o.add_argument(
        "--ignore-certificate-error"
    )
    o.add_argument(
        "--ignore-ssl-errors"
    )
    o.add_experimental_option(
        'mobileEmulation', 
        {
       'deviceName':'Pixel 7'
       }
    )
    o.add_argument('--headless')
    o.add_argument('--no-sandbox')
    o.add_argument('--disable-gpu')
    o.add_argument('--disable-dev-shm-usage')
    s=Service(chrome_driver)
    iu, im, ih, ss = '', '', '', 2
    try:
        driver = webdriver.Chrome(
            # executable_path=chrome_driver,
            service=s,
            options = o
        )
        driver.set_page_load_timeout(
            15
        )
    
        # try:
        driver.get(
            link
        )
        sleep(
            5
        )
        driver.execute_script(
            "window.stop();"
        )
        ss = 1
        try:
            iu=um(
                driver.get_screenshot_as_png(),
                d+'.png'
            )
        except:
            pass
        try:
            im=um(
                driver.execute_cdp_cmd(
                    'Page.captureSnapshot', 
                    {}
                )[
                    'data'
                ].encode(
                    'utf-8'
                ),
                d+'.mhtml'
            )
        except:
            pass
        h = driver.page_source.encode(
            'utf-8'
        )
        try:
            ih=um(
                h,
                d+'.html'
            )
        except:
            pass
        return h, iu, im, ih, ss
    except Exception as e:
        print(
            e.__traceback__.tb_frame.f_globals['__file__'],
            e.__traceback__.tb_lineno,
            e
        )
        return h, iu, im, ih, ss
    finally:
        driver.quit()
              
def pc(path):
    for c in r'<>/\|:*? ': path = path.replace(c, '_')
    return path  

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        
c = Consumer(
    kafka_consumer
)
p=Producer(
    kafka_producer
)
c.subscribe(
    [
     kafka_input_topic
    ]
)

while True:
    try:
        mi = c.poll(1.0)
    
        if mi is None:
            continue
        if mi.error():
            print("Consumer error: {}".format(mi.error()))
            continue
        ki = loads(mi.value().decode('utf-8'))
        
        print('Received message: {}'.format(ki))
        ko = {
            'excelId':ki['excelId'],
            'wzId':ki['wzId'],
            'dxId':ki["dxId"],
            'dxYhType':ki['dxYhType'],
            'url':ki["url"],
            'dialStartTime':ki['dialStartTime'],
            'dialEndTime':0,
            'dialIP':'',
            'status':2,
            'location':'',
            'wzIP':'',
            'jumpCount':'',
            'recordInfo':'',
            'imgUrl':'',
            'htmlUrl':'',
            'mhtmlUrl':''
        }
        try:
            ko['dialIP']=loads(
                urlopen(
                    'http://localhost:5010/get/'
                ).read()
            )['proxy'].split(
                ':'
            )[0]
        except Exception as e:
            print(
                e.__traceback__.tb_frame.f_globals['__file__'],
                e.__traceback__.tb_lineno,
                e
            )
            pass
        try:
            ko['wzIP']=gethostbyname(
                ki['url'].split(
                    '://'
                )[-1]
            )
        except Exception as e:
            print(
                e.__traceback__.tb_frame.f_globals['__file__'],
                e.__traceback__.tb_lineno,
                e
            )
            pass
        try:
            ko['location']=loads(
                get(
                    'https://whois.pconline.com.cn/ipJson.jsp?ip={}&json=true'.format(
                        ko['wzIP']
                    )
                ).text
            )[
              'addr'
          ].strip()
        except Exception as e:
            print(
                e.__traceback__.tb_frame.f_globals['__file__'],
                e.__traceback__.tb_lineno,
                e
            )
            pass
        if 'https'==ki['url'][:5]:
            l=ki['url'].replace(
                'https', 
                'http',
                1
            )
        elif 'http'!=ki['url'][:4]:
            l='http://'+ki['url']
        else:
            l=ki['url']
        try:
            dp = pc(
                ki[
                    'url'
                ]
            )
            ht = lh(
                l, 
                dp
            )    
            ko['imgUrl']=ht[1]
            ko['htmlUrl']=ht[3]
            ko['mhtmlUrl']=ht[2]
            ko['status']=ht[4]
        except Exception as e:
            print(
                e.__traceback__.tb_frame.f_globals['__file__'],
                e.__traceback__.tb_lineno,
                e
            )
            pass
        try:
            ko[
                'jumpCount'
            ]=ht[0].decode(
                'utf-8'
                ).count(
                'http'
            )
        except:
            pass
        try:
            ko[
                'recordInfo'
            ]=BeautifulSoup(
                ht[0],
                features="lxml"
            ).find(
                href=re.compile(
                    "www.beian.gov.cn"
                )
            ).get_text()
        except:
            pass
        ko[
           'dialEndTime'
        ]=int(
              round(
                  time()*1000
              )
          )
        mo = dumps(
            ko,
            indent=True,
            ensure_ascii=False
        )
        print(
            mo
        )
        p.poll(0)
        p.produce(
            kafka_output_topic,
            mo,
            callback=delivery_report
        )
    except Exception as e:
        print(
            e.__traceback__.tb_frame.f_globals['__file__'],
            e.__traceback__.tb_lineno,
            e
        )
        pass
    finally:
        sleep(
            2
        )
        continue

c.close()
p.flush()

