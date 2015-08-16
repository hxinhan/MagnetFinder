#!/usr/bin/python
#coding=utf-8

__AUTOR__= "HansonHH"
__DATA__= "13/08/15"
__VERSAO__= "1.0.1"
__GITHUB__= "https://github.com/HansonHH"

"""
Copyright (C) 2015 Xin Han 
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
GNU General Public License for more details.
"""
import sys
import urllib
import urllib2
import re 
import random
import threading 
import time
import os
import webbrowser
from Proxy import get_proxy_list
from Proxy import proxy_setting
from Proxy import proxy_test
from bs4 import BeautifulSoup
from Class import FanHao

type = sys.getfilesystemencoding()

def cili_parse(fanhao,proxy_headers):
    global cili_fanhaos
    cili_fanhaos = []
    try:
        fanhao_url = 'http://www.cili.tv/search/%s_ctime_1.html'%urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=5)
        fanhao_html = response.read()
    except Exception:
        return cili_fanhaos

    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find_all("div",attrs={"class":"item"})
    if soup_items:
        for item in soup_items:
            title = item.a.text.strip()
            info = item.find("div",attrs={"class":"info"}) 
            spans = info.find_all("span")
            file_size = str(spans[1].b.text)
            downloading_count = int(str(spans[2].b.string))
            magnet_url = str(spans[3].find("a").get('href'))
            resource = 'Cili'
            resource_url = 'http://www.cili.tv'
            fanhao = FanHao(title,file_size,downloading_count,None,magnet_url,resource,resource_url)
            cili_fanhaos.append(fanhao)
    return cili_fanhaos

def btdb_parse(fanhao,proxy_headers):
    global btdb_fanhaos
    btdb_fanhaos = []
    try:
        fanhao_url = 'http://btdb.in/q/%s/'%urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return btdb_fanhaos

    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find_all("li",attrs={"class":"search-ret-item"})
    if soup_items:
        for item in soup_items:
            title = item.find("h1").find("a").get("title")
            info = item.find("div",attrs={"class":"item-meta-info"}).find_all("span",attrs={"class":"item-meta-info-value"})
            file_size = info[0].text
            downloading_count = int(info[-1].text)
            file_number = int(info[1].text)
            magnet_url = item.find("div",attrs={"class":"item-meta-info"}).find("a",attrs={"class":"magnet"}).get("href")
            resource = 'BTDB'
            resource_url = 'http://btdb.in'
            fanhao = FanHao(title,file_size,downloading_count,file_number,magnet_url,resource,resource_url)
            btdb_fanhaos.append(fanhao)
    return btdb_fanhaos

def btbook_parse(fanhao,proxy_headers):
    global btbook_fanhaos
    btbook_fanhaos = []
    try:
        fanhao_url = 'http://www.btbook.net/search/'+urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))+'.html'
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return btbook_fanhaos

    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find_all("div",attrs={"class":"search-item"})
    if soup_items:
        for item in soup_items:
            title = item.find("h3").find("a").find("b").text
            info = item.find("div",attrs={"class":"item-bar"}).find_all("span")
            file_size = info[2].b.text
            downloading_count = int(info[3].b.text)
            magnet_url = item.find("div",attrs={"class":"item-bar"}).find("a").get("href")
            resource = 'Btbook'
            resource_url = 'http://www.btbook.net'
            fanhao = FanHao(title,file_size,downloading_count,None,magnet_url,resource,resource_url)
            btbook_fanhaos.append(fanhao)    
    return btbook_fanhaos

def btcherry_parse(fanhao,proxy_headers):
    global btcherry_fanhaos
    btcherry_fanhaos = []
   
    try:
        fanhao_url = 'http://www.btcherry.net/search?keyword='+urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return btcherry_fanhaos
    
    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find_all("div",attrs={"class":"r"})
    if soup_items:
        for item in soup_items:
            try:
                title = item.find("h5",attrs={"class":"h"}).text
                info = item.find("div").find_all("span")
                file_size = info[2].find("span",attrs={"class":"prop_val"}).text
                file_number = int(info[4].find("span",attrs={"class":"prop_val"}).text)
                magnet_url = item.find("div").find("a").get("href")
            except Exception:
                pass
             
            resource = 'BTCherry'
            resource_url = 'http://www.btcherry.net'
            fanhao = FanHao(title,file_size,None,file_number,magnet_url,resource,resource_url)
            btcherry_fanhaos.append(fanhao)
    return btcherry_fanhaos

def zhongziIn_parse(fanhao,proxy_headers):
    global zhongziIn_fanhaos
    zhongziIn_fanhaos = []
   
    try:
        fanhao_url = 'http://www.zhongzi.in/s/'+urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return zhongziIn_fanhaos
    
    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find("div",attrs={"class":"wx_list"}).find_all("li")
    
    if soup_items:
        for item in soup_items:
            title = item.find("a").get('title')
            info = item.find("span",attrs={"class":"j_size"})
            file_size = info.text.split(":")[1] 
            magnet_url = info.find("a").get('href') 
            resource = 'zhongzi.in'
            resource_url = 'http://www.zhongzi.in'
            fanhao = FanHao(title,file_size,None,None,magnet_url,resource,resource_url)
            zhongziIn_fanhaos.append(fanhao)
    return zhongziIn_fanhaos
    
def micili_parse(fanhao,proxy_headers):
    global micili_fanhaos
    micili_fanhaos = []
   
    try:
        fanhao_url = 'http://www.micili.com/list/'+urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))+'/?c=&s=create_time'
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return micili_fanhaos
    
    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find("ul",attrs={"class":"collection z-depth-1"}).find_all("li")

    if soup_items:
        for item in soup_items:
            title = item.find("h6").find("a").get('title')
            info = item.find("span",attrs={"class":"mt10"})
            file_number=int(info.text.split(':')[1].split(u'大小')[0].strip())
            file_size=info.text.split(':')[2].split(u'请求数')[0].strip()
            downloading_count=int(info.text.split(u'请求数:')[1].split(u'磁力链接')[0].strip())
            magnet_url = info.find("a").get('href')
            resource = 'micili'
            resource_url = 'http://www.micili.com'
            fanhao = FanHao(title,file_size,downloading_count,file_number,magnet_url,resource,resource_url)
            micili_fanhaos.append(fanhao)
    return micili_fanhaos

def btku_parse(fanhao,proxy_headers):
    global btku_fanhaos
    btku_fanhaos = []
   
    try:
        fanhao_url = 'http://www.btku.me/q/%s/'%urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return btku_fanhaos
    
    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find("div",attrs={"id":"search_Results"}).find_all("li",attrs={"class":"results"})
    if soup_items:
        for item in soup_items:
            title = item.find("h2").find("a").text
            info = item.find("p",attrs={"class":"resultsIntroduction"})
            file_number = int(info.find_all("label")[0].string)
            file_size = info.find_all("label")[1].string
            downloading_count = int(info.find_all("label")[2].string)
            magnet_url = info.find("span",attrs={"class":"downLink"}).find_all("a")[1].get('href')
            resource = 'BTKU'
            resource_url = 'http://www.btku.me'
            fanhao = FanHao(title,file_size,downloading_count,file_number,magnet_url,resource,resource_url)
            btku_fanhaos.append(fanhao)
    return btku_fanhaos

def Qululu_parse(fanhao,proxy_headers):
    global Qululu_fanhaos
    Qululu_fanhaos = []
   
    try:
        fanhao_url = 'http://www.qululu.cn/search1/b/%s/1/hot_d'%fanhao.decode(sys.stdin.encoding).encode('utf8').encode('hex')
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return Qululu_fanhaos
    
    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find("ul",attrs={"class":"mlist"}).find_all("li")
    if soup_items:
        for item in soup_items:
            title = item.find("div",attrs={"class":"T1"}).find("a").string
            title = re.sub('<span class="mhl">','',re.sub('</span>','',title.decode('hex')))
            info = item.find("dl",attrs={"class":"BotInfo"}).find("dt").find_all("span")
            file_size = info[0].string.replace(' ','')
            file_number = int(info[1].string)
            downloading_count = int(info[3].string)
            magnet_url = item.find("div",attrs={"class":"dInfo"}).find("a").get('href')
            resource = 'Qululu'
            resource_url = 'http://www.qululu.cn'
            fanhao = FanHao(title,file_size,downloading_count,file_number,magnet_url,resource,resource_url)
            Qululu_fanhaos.append(fanhao)
    return Qululu_fanhaos

def nimasou_parse(fanhao,proxy_headers):
    global nimasou_fanhaos
    nimasou_fanhaos = []
   
    try:
        fanhao_url = 'http://www.nimasou.com/l/%s-hot-desc-1'%urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
        response = urllib2.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return nimasou_fanhaos
    
    soup = BeautifulSoup(fanhao_html)
    try:
        soup_items = soup.find("table",attrs={"class":"table"}).find_all("tr")
    except Exception:
        return nimasou_fanhaos
    if soup_items:
        for item in soup_items:
            title = item.find("td",attrs={"class":"x-item"}).find("a",attrs={"class":"title"}).text
            info = item.find("td",attrs={"class":"x-item"}).find("div",attrs={"class":"tail"}).text.split(':')
            file_size = info[2].split(' ')[1] + info[2].split(' ')[2]
            downloading_count = int(info[3].split(' ')[1])
            magnet_url = item.find("td",attrs={"class":"x-item"}).find("div",attrs={"class":"tail"}).find("a").get('href')
            resource = 'NiMaSou'
            resource_url = 'http://www.nimasou.com'
            fanhao = FanHao(title,file_size,downloading_count,None,magnet_url,resource,resource_url)
            nimasou_fanhaos.append(fanhao)
    return nimasou_fanhaos

def print_result(fanhaos):
    if fanhaos:
        for fanhao in fanhaos:
            try:
                print u'名称:%s'%fanhao.title
                print u'文件大小:%s'%fanhao.file_size
                if fanhao.downloading_count:
                    print u'热度:%d'%fanhao.downloading_count
                else:
                    print u'热度:--'
                if fanhao.file_number:
                    print u'文件数:%s'%str(fanhao.file_number)
                else:
                    print u'文件数:--'
                print u'磁力链接:%s'%fanhao.magnet_url
                print u'来源:%s'%fanhao.resource
                print '-'*40
            except Exception:
                pass
        print u'资源数:%d个'%len(fanhaos)
    else:
        print u'抱歉未找到相关资源！'


def set_headers():
    headers1 = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','Accept':'text/html;q=0.9,*/*;q=0.8','Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}
    headers2 = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5'}
    headers3 = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'}
    headers4 = {'User-Agent:':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
    headers = [headers1,headers2,headers3,headers4]
    return random.choice(headers)
    

def create_url(fanhaos):
    fanhao_html = open("Index.html","r").read()
    soup = BeautifulSoup(fanhao_html)
    fanhao_tbody_html = soup.find("tbody")
    for index,fanhao in enumerate(fanhaos):
        tr_tag = soup.new_tag('tr')
        fanhao_tbody_html.insert(0,tr_tag)
        
        fanhao_tbody_tr = fanhao_tbody_html.find('tr')
        th_tag = soup.new_tag('th')
        th_tag.string = str(index+1)
        fanhao_tbody_tr.insert(0,th_tag)
        
        title_tag = soup.new_tag('td')
        title_tag.string = fanhao.title
        fanhao_tbody_tr.insert(1,title_tag)
        
        file_size_tag = soup.new_tag('td')
        file_size_tag.string = fanhao.file_size
        fanhao_tbody_tr.insert(2,file_size_tag)
        
        downloading_count_tag = soup.new_tag('td')
        if fanhao.downloading_count is not None:
            downloading_count_tag.string = str(fanhao.downloading_count)
        else:
            downloading_count_tag.string = '--'
        fanhao_tbody_tr.insert(3,downloading_count_tag)

        file_number_tag = soup.new_tag('td')
        if fanhao.file_number is not None:
            file_number_tag.string = str(fanhao.file_number)
        else:
            file_number_tag.string = '--'
        fanhao_tbody_tr.insert(4,file_number_tag)
        
        magnet_url_tag = soup.new_tag('td')
        magnet_url_tag['class'] = 'magnet'
        #magnet_url_tag['style'] = 'max-width:100px;'
        fanhao_tbody_tr.insert(5,magnet_url_tag)
        fanhao_magnet_td = fanhao_tbody_tr.find('td',attrs={'class':'magnet'})
        magnet_url_a = soup.new_tag('a',href=fanhao.magnet_url)
        #magnet_url_a.string = fanhao.magnet_url
        magnet_url_a.string = u'点击下载'
        magnet_url_a['class'] = 'btn btn-success'
        fanhao_magnet_td.insert(0,magnet_url_a)

        resource_tag = soup.new_tag('td')
        resource_tag.string = fanhao.resource
        fanhao_tbody_tr.insert(6,resource_tag)

    return soup

def open_browser(soup):
    new_html = file("MagnetFinder.html","wb")
    new_html.write(str(soup))
    new_html.close()
    
    html_url = 'file://'+os.getcwd()+'/MagnetFinder.html'
    webbrowser.open(html_url,new=2)

if __name__ == '__main__':
    print '*'*40
    print '*'
    print '* Magnet Finder'
    print '*'
    print '* V 1.0.1'
    print '* Coded by Hanson'
    print '* Github https://github.com/HansonHH'
    print '*'
    print '*'*40

    enable_proxy = False

    # Do you want to configure proxy 
    proxy_select = raw_input(unicode('是否设置代理?(Y/N):','utf-8').encode(type))
    if proxy_select == 'Y' or proxy_select == 'y':
        enable_proxy = True
    else:
        enable_proxy = False

    if enable_proxy == True:
        proxy_list = get_proxy_list()
        proxy_configured = False
        while not proxy_configured:
            current_proxy,proxy_list = proxy_setting(proxy_list)
            proxy_configured = proxy_test(proxy_configured)
        print 'Current Proxy Address %s'%current_proxy.proxy_address
        print 'Current Proxy Location %s'%current_proxy.country
    
    while True:
        # Input title to search
        fanhao = raw_input(unicode('请输入想要搜索的番号或标题:','utf-8').encode(type))
        # Counting time start point 
        start_time = time.time()
        
        threads = []
        
        btdb_thread = threading.Thread(target=btdb_parse,args=(fanhao,set_headers(),))
        threads.append(btdb_thread)
        
        btbook_thread = threading.Thread(target=btbook_parse,args=(fanhao,set_headers(),))
        threads.append(btbook_thread)
        
        cili_thread = threading.Thread(target=cili_parse,args=(fanhao,set_headers(),))
        threads.append(cili_thread)
        
        btcherry_thread = threading.Thread(target=btcherry_parse,args=(fanhao,set_headers(),))
        threads.append(btcherry_thread)
        
        zhongziIn_thread = threading.Thread(target=zhongziIn_parse,args=(fanhao,set_headers(),))
        threads.append(zhongziIn_thread)
        
        micili_thread = threading.Thread(target=micili_parse,args=(fanhao,set_headers(),))
        threads.append(micili_thread)
        
        btku_thread = threading.Thread(target=btku_parse,args=(fanhao,set_headers(),))
        threads.append(btku_thread)

        Qululu_thread = threading.Thread(target=Qululu_parse,args=(fanhao,set_headers(),))
        threads.append(Qululu_thread)
        
        nimasou_thread = threading.Thread(target=nimasou_parse,args=(fanhao,set_headers(),))
        threads.append(nimasou_thread)

        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        fanhaos=btdb_fanhaos+btbook_fanhaos+cili_fanhaos+btcherry_fanhaos+zhongziIn_fanhaos+micili_fanhaos+btku_fanhaos+Qululu_fanhaos+nimasou_fanhaos 
        #fanhaos = nimasou_fanhaos 

        # Sorting bt descending
        fanhaos.sort(key=lambda fanhao:fanhao.downloading_count)
        
        print_result(fanhaos)
        
        # Counting time end point
        finish_time = time.time()
        elapsed = finish_time - start_time
        print u'耗时:%s 秒'%elapsed

        soup = create_url(fanhaos)
        open_browser(soup)
