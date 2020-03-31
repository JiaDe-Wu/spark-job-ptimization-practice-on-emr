#!/usr/bin/env python
# coding: utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
from zipfile import ZipFile
from io import BytesIO
import requests
import os

def payloadCreation(user, password):
    creds={'username': user,'password': password }
    return creds
def getFilesFromFreddieMac(payload, startY, endY):
    # 定义要遍历URL.
    url='https://freddiemac.embs.com/FLoan/secure/auth.php'
    postUrl='https://freddiemac.embs.com/FLoan/Data/download.php'
    # 定义本地下载到本地文件夹.
    target_folder = 'TestData'
    # 定义session，进行登录.
    s = requests.Session()
    preUrl = s.post(url, data=payload)
    payload2={'accept': 'Yes','acceptSubmit':'Continue','action':'acceptTandC'}
    finalUrl=s.post(postUrl,payload2)
    # 定义遍历目标压缩包.
    linkhtml =finalUrl.text
    allzipfiles=BeautifulSoup(linkhtml, "html.parser>)
    ziplist=allzipfiles.find_all('a')
    # 定义年份变量.
    year_list = []
    start_year = startY
    end_year = endY
    for i in range(int(start_year),int(end_year)+1):
        year_list.append(str(i))
    # 拼出最终下载链接.
    historicaldata_links=[]
    local_path=str(os.getcwd())+"/" + target_folder
    for year in year_list:
        for li in ziplist:
            if year in li.text and 'historical' in li.text:
                final_link ='https://freddiemac.embs.com/FLoan/Data/' + li.get('href')
                print(final_link)
                historicaldata_links.append(final_link)
    # 循环下载和解压.
    for lin in historicaldata_links:
        r = s.get(lin)
        z = ZipFile(BytesIO(r.content))
        z.extractall(local_path)
        print('.')
def main():
    print("Starting")
    start_year = '1999'
    end_year = '2019'
    user = 'xxxx@xxxx.com'
    password = 'xxxxxx'
    payload=payloadCreation(user,password)
    getFilesFromFreddieMac(payload, start_year, end_year)
if __name__ == '__main__':
    main()
