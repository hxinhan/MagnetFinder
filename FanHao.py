#-*- coding:utf-8 -*
import urllib
import urllib2
import re 
import random
import cookielib
from bs4 import BeautifulSoup
from Class import FanHao
from Class import ProxyServer 

enable_proxy = False

print '#'*40
print '# FanHao'
print '#'*40

proxy_select = raw_input("Do you want to configure proxy?(Y/N):")
if proxy_select == 'Y' or proxy_select == 'y':
    enable_proxy = True
else:
    enable_proxy = False

'''
class ProxyServer:
    def __init__(self,proxy_address,proxy_http,speed,proxy_type,country):
        self.proxy_address=proxy_address
        self.proxy_http=proxy_http
        self.speed=speed
        self.proxy_type=proxy_type
        self.country=country

class FanHao:
    def __init__(self,title,file_size,downloading_count,magnet_url):
        self.title = title
        self.file_size = file_size
        self.downloading_count = downloading_count
        self.magnet_url = magnet_url
'''

def proxy_test():
    print 'Proxy Testing...'
    test_headers = {'User-Agent:':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
    test_url = 'http://www.google.com'
    #test_url2 = 'http://www.whereisip.net/'
    test_request = urllib2.Request(test_url,headers=test_headers)
    try:
        test_response = urllib2.urlopen(test_request,timeout=10)
        #print test_response.getcode()
        if test_response.getcode()==200:
            #print '-'*200 
            #test_request2 = urllib2.Request(test_url2,headers=test_headers)
            #test_response2 = urllib2.urlopen(test_request2,timeout=10)
            #print test_response2.read()
            print u'Configured proxy successfully!'
            global proxy_configured 
            proxy_configured = True
    except Exception:
        print u'Failed to configure proxy!'
    
def find_highest_speed(proxy_list):
    temp_proxy = None
    highest_speed = 0
    for proxy_server in proxy_list:
        proxy_server_speed = proxy_server.speed.split('kbit')[0]
        print 'proxy_server.proxy_address = %s'%proxy_server.proxy_address
        print 'proxy_server.speed = %skbit/s'%proxy_server_speed
        if proxy_server_speed !='-':
            if float(proxy_server_speed) > highest_speed:
                highest_speed = float(proxy_server_speed)
                temp_proxy = proxy_server
    print '*'*40
    print 'Temp Proxy Address %s'%temp_proxy.proxy_address
    print 'Temp Proxy Speed %s/s'%temp_proxy.speed
    print '*'*40
    proxy_list.remove(temp_proxy)
    return temp_proxy,proxy_list

def get_proxy_list():
    proxy_headers = {'User-Agent:':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
    proxy_url = 'http://proxy-list.org/english/index.php'
    proxy_request = urllib2.Request(proxy_url,headers=proxy_headers)

    try:
        response = urllib2.urlopen(proxy_request,timeout=10)
        html = response.read()
    except urllib2.HTTPError,e:
        print e.code

    name_ul = re.compile("(?isu)<ul>(.*?)</ul>")
    name_li = re.compile("(?isu)<li[^>]*>(.*?)</li>")

    proxy_list_txt = open('proxy_list.txt','w')
    proxy_list=[]
    
    for row in name_ul.findall(html):
        proxy_address = ''.join(name_li.findall(row)[0:1])
        proxy_http = ''.join(name_li.findall(row)[1:2])
        speed = ''.join(name_li.findall(row)[2:3])
        proxy_type = ''.join(name_li.findall(row)[3:4])
        name_country = re.compile('title="(.*?)"')
        country_name=None
        for country in name_li.findall(row)[4:5]:
            country_name = ''.join(name_country.findall(country))
            if '&nbsp;' in country_name:
                country_name=country_name.split('&nbsp;')[0]+' '+country_name.split('&nbsp;')[1]
        
        proxy_server = ProxyServer(proxy_address,proxy_http,speed,proxy_type,country_name)
        proxy_list.append(proxy_server)
        proxy_list_txt.write(proxy_server.proxy_address+'\n')
        
    proxy_list_txt.close()
    
    return proxy_list

def proxy_setting(proxy_list):
    try:
        random_proxy,new_proxy_list = find_highest_speed(proxy_list)
    except Exeception:
        print 'Failed to Configure Proxy!'

    proxy_handler = urllib2.ProxyHandler({'http':'http://%s'%random_proxy.proxy_address})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    print 'Proxy Configuring...'
    return random_proxy,new_proxy_list

if enable_proxy == True:
    proxy_list = get_proxy_list()
    proxy_configured = False
    while not proxy_configured:
        current_proxy,proxy_list = proxy_setting(proxy_list)
        proxy_test()
        #proxy_configured = True
    print 'Current Proxy Address %s'%current_proxy.proxy_address
    print 'Current Proxy Location %s'%current_proxy.country

fanhao = raw_input("请输入想要查找的番号:")

test_headers = {'Host':'www.torrentkitty.org','Connection':'keep-alive','Cache-Control':'max-age=0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4','Accept-Language':'q=0.8,en','If-None-Match':'4202560e','Referer':'http://www.torrentkitty.org/search/','If-Modified-Since':'Sat, 08 Aug 2015 18:47:00 GMT','Cookie':'incap_ses_200_146743=QUn7VypDaye+j49SyYvGAoOpx1UAAAAAJuqGCnYai0FaUBNeI5y23Q==;'}

proxy_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','Accept':'text/html;q=0.9,*/*;q=0.8','Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}
#fanhao_url = 'http://www.cili.tv/search/'+fanhao+'_ctime_1.html'
fanhao_url = 'http://www.torrentkitty.org/search/SNIS-338/'
#fanhao_url = 'http://www.torrentkitty.org/css/font.css'
        
proxy_request = urllib2.Request(fanhao_url,headers=test_headers)
#proxy_request = urllib2.Request(fanhao_url,headers=proxy_headers)
response = urllib2.urlopen(proxy_request) #timeout=10
fanhao_html = response.read()
print fanhao_html
print response.info()



cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
req = urllib2.Request(fanhao_url,headers=test_headers)
result = opener.open(req)
#print result.read()
for item in cookie:
    print 'Name = '+item.name
    print 'Value = '+item.value


#print fanhao_html.decode('gb2312','ignore').encode('utf-8')

'''
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
        fanhao = FanHao(title,file_size,downloading_count,magnet_url)
        fanhaos.append(fanhao)
    
    for fanhao in fanhaos:
        print u'名称:'+fanhao.title
        print u'文件大小:'+fanhao.file_size
        print u'热度:'+fanhao.downloading_count
        print u'磁力链接:'+fanhao.magnet_url
        print '-'*40
    #print u'资源数:'+str(len(fanhaos))+u'个'
    print u'资源数:%d个'%len(fanhaos)
else:
    print u'抱歉未找到相关资源！'
'''


    

