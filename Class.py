#-*- coding:utf-8 -*

class ProxyServer:
    def __init__(self,proxy_address,proxy_http,speed,proxy_type,country):
        self.proxy_address=proxy_address
        self.proxy_http=proxy_http
        self.speed=speed
        self.proxy_type=proxy_type
        self.country=country

class FanHao:
    def __init__(self,title,file_size,downloading_count,magnet_url,resource):
        self.title = title
        self.file_size = file_size
        self.downloading_count = downloading_count
        self.magnet_url = magnet_url
        self.resource = resource
