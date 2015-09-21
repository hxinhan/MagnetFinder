import urllib
import urllib2
import re 
from Class import ProxyServer 

def proxy_test(proxy_configured):
    print 'Proxy Testing...'
    test_headers = {'User-Agent:':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
    test_url = 'http://www.google.com'
    test_request = urllib2.Request(test_url,headers=test_headers)
    try:
        test_response = urllib2.urlopen(test_request,timeout=10)
        if test_response.getcode()==200:
            print u'Configured proxy successfully!'
            return True
        else:
            return False   
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
    except Exception:
        print 'Failed to Configure Proxy!'

    proxy_handler = urllib2.ProxyHandler({'http':'http://%s'%random_proxy.proxy_address})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    print 'Proxy Configuring...'
    return random_proxy,new_proxy_list
