#-*- coding:utf-8 -*

class ProxyServer:
    __slots__ = ('proxy_address','proxy_http','speed','proxy_type','country')
    def __init__(self,proxy_address,proxy_http,speed,proxy_type,country):
        self.proxy_address=proxy_address
        self.proxy_http=proxy_http
        self.speed=speed
        self.proxy_type=proxy_type
        self.country=country

class FanHao:
    __slots__ = ('title','file_size','downloading_count','file_number','magnet_url','resource','resource_url')
    def __init__(self,title,file_size,downloading_count,file_number,magnet_url,resource,resource_url):
        self.title = title
        self.file_size = file_size
        self.downloading_count = downloading_count
        self.file_number = file_number
        self.magnet_url = magnet_url
        self.resource = resource
        self.resource_url = resource_url
    #def __repr__(self):
    #    return repr((self.title,self.file_size,self.downloading_count,self.magnet_url,self.resource,self.resource_url))
