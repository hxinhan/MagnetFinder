#!/usr/bin/python
#coding=utf-8

__AUTOR__= "HansonHH"
__DATA__= "13/08/15"
__VERSAO__= "1.0.1"
__GITHUB__= "https://github.com/HansonHH"

"""
Copyright (C) 2015  Franco Colombino
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
import cookielib
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
    fanhao_url = 'http://www.cili.tv/search/%s_ctime_1.html'%urllib.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
    proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
    response = urllib2.urlopen(proxy_request,timeout=20)
    fanhao_html = response.read()

    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find_all("div",attrs={"class":"item"})
    if soup_items:
        fanhaos = []
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
            fanhaos.append(fanhao)
        return fanhaos
    else:
        return []

def btdb_parse(fanhao,proxy_headers):
    fanhao_url = 'http://btdb.in/q/%s/'%urllib.quote(fanhao.decode(sys.stdin.encoding)
.encode('utf8'))
    proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
    response = urllib2.urlopen(proxy_request,timeout=20)
    fanhao_html = response.read()

    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find_all("li",attrs={"class":"search-ret-item"})
    if soup_items:
        fanhaos = []
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
            fanhaos.append(fanhao)
        return fanhaos
    else:
        return []

def btbook_parse(fanhao,proxy_headers):
    fanhao_url = 'http://www.btbook.net/search/'+urllib.quote(fanhao.decode(sys.stdin.encoding)
.encode('utf8'))+'.html'
    proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
    response = urllib2.urlopen(proxy_request,timeout=20)
    fanhao_html = response.read()

    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find_all("div",attrs={"class":"search-item"})
    if soup_items:
        fanhaos = []
        for item in soup_items:
            title = item.find("h3").find("a").find("b").text
            info = item.find("div",attrs={"class":"item-bar"}).find_all("span")
            file_size = info[2].b.text
            downloading_count = int(info[3].b.text)
            magnet_url = item.find("div",attrs={"class":"item-bar"}).find("a").get("href")
            resource = 'Btbook'
            resource_url = 'http://www.btbook.net'
            fanhao = FanHao(title,file_size,downloading_count,None,magnet_url,resource,resource_url)
            fanhaos.append(fanhao)
        return fanhaos
    else:
        return []

def btcherry_parse(fanhao,proxy_headers):
    fanhao_url = 'http://www.btcherry.net/search?keyword='+urllib.quote(fanhao.decode(sys.stdin.encoding)
.encode('utf8'))
    proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
    response = urllib2.urlopen(proxy_request,timeout=20)
    fanhao_html = response.read()

    soup = BeautifulSoup(fanhao_html)
    soup_items = soup.find_all("div",attrs={"class":"r"})
    if soup_items:
        fanhaos = []
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
            fanhaos.append(fanhao)
        return fanhaos
    else:
        return []

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
        if fanhao.downloading_count:
            downloading_count_tag.string = str(fanhao.downloading_count)
        else:
            downloading_count_tag.string = '--'
        fanhao_tbody_tr.insert(3,downloading_count_tag)

        file_number_tag = soup.new_tag('td')
        if fanhao.file_number:
            file_number_tag.string = str(fanhao.file_number)
        else:
            file_number_tag.string = '--'
        fanhao_tbody_tr.insert(4,file_number_tag)
        
        magnet_url_tag = soup.new_tag('td')
        magnet_url_tag['class'] = 'magnet'
        fanhao_tbody_tr.insert(5,magnet_url_tag)
        fanhao_magnet_td = fanhao_tbody_tr.find('td',attrs={'class':'magnet'})
        magnet_url_a = soup.new_tag('a',href=fanhao.magnet_url)
        magnet_url_a.string = fanhao.magnet_url
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
    
        start_time = time.time()
    
        cili_fanhaos = []
        try:
            cili_fanhaos = cili_parse(fanhao,set_headers())
        except Exception:
            pass
    
        btdb_fanhaos = []
        try:
            btdb_fanhaos = btdb_parse(fanhao,set_headers())
        except Exception:
            pass
    
        btbook_fanhaos = [] 
        try:
            btbook_fanhaos = btbook_parse(fanhao,set_headers())
        except Exception:
            pass
    
        btcherry_fanhaos = []
        try:
            btcherry_fanhaos = btcherry_parse(fanhao,set_headers())
        except Exception:
            pass
    
        fanhaos = btdb_fanhaos+cili_fanhaos+btbook_fanhaos+btcherry_fanhaos
        # Sorting bt descending
        fanhaos.sort(key=lambda fanhao:fanhao.downloading_count)
    
        print_result(fanhaos)

        finish_time = time.time()
        elapsed = finish_time - start_time
        print u'耗时:%s 秒'%elapsed

        soup = create_url(fanhaos)
        open_browser(soup)
