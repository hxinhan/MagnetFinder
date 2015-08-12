#-*- coding:utf-8 -*
import urllib
import urllib2
import re 
import random
import cookielib
from Proxy import get_proxy_list
from Proxy import proxy_setting
from Proxy import proxy_test
from bs4 import BeautifulSoup
from Class import FanHao



def cili_parse(fanhao):
    proxy_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','Accept':'text/html;q=0.9,*/*;q=0.8','Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}
    fanhao_url = 'http://www.cili.tv/search/'+fanhao+'_ctime_1.html'
    proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
    response = urllib2.urlopen(proxy_request,timeout=20) #timeout=10
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
            downloading_count = str(spans[2].b.string)
            magnet_url = str(spans[3].find("a").get('href'))
            resource = 'Cili'
            resource_url = 'http://www.cili.tv'
            fanhao = FanHao(title,file_size,downloading_count,magnet_url,resource,resource_url)
            fanhaos.append(fanhao)
        
        return fanhaos

def print_result(fanhaos):
    
    if fanhaos:
        for fanhao in fanhaos:
            print u'名称:'+fanhao.title
            print u'文件大小:'+fanhao.file_size
            print u'热度:'+fanhao.downloading_count
            print u'磁力链接:'+fanhao.magnet_url
            print u'来源:'+fanhao.resource
            print '-'*40
        print u'资源数:%d个'%len(fanhaos)
    else:
        print u'抱歉未找到相关资源！'

'''
test_headers = {'Host':'www.torrentkitty.org','Connection':'keep-alive','Cache-Control':'max-age=0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4','Accept-Language':'q=0.8,en','If-None-Match':'4202560e','Referer':'http://www.torrentkitty.org/search/','If-Modified-Since':'Sat, 08 Aug 2015 18:47:00 GMT','Cookie':'incap_ses_200_146743=QUn7VypDaye+j49SyYvGAoOpx1UAAAAAJuqGCnYai0FaUBNeI5y23Q==;'}

fanhao_url = 'http://www.torrentkitty.org/search/SNIS-338/'
#fanhao_url = 'http://www.torrentkitty.org/css/font.css'

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
req = urllib2.Request(fanhao_url,headers=test_headers)
result = opener.open(req)
#print result.read()
for item in cookie:
    print 'Name = '+item.name
    print 'Value = '+item.value
'''

'''
print '-'*200 
test_headers = {'User-Agent:':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
test_url2 = 'http://btdb.in/q/snis-338/'
test_request2 = urllib2.Request(test_url2,headers=test_headers)
test_response2 = urllib2.urlopen(test_request2,timeout=20)
print test_response2.read()
'''

#print fanhao_html.decode('gb2312','ignore').encode('utf-8')


if __name__ == '__main__':
    print '#'*40
    print '# FanHao'
    print '#'*40

    enable_proxy = False

    proxy_select = raw_input("Do you want to configure proxy?(Y/N):")
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
    
    fanhao = raw_input("请输入想要查找的番号:")

    fanhaos = cili_parse(fanhao)
    
    print_result(fanhaos)

