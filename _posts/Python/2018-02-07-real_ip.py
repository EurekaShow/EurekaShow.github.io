#!/usr/bin/python
# -*- coding:utf8 -*-
 
import urllib2
import re
 
def get_real_ip():
    url = urllib2.urlopen("http://txt.go.sohu.com/ip/soip")
    text = url.read()
    ip = re.findall(r'\d+.\d+.\d+.\d+',text)
    
    #print ip[0]
    return ip[0]

if __name__ == "__main__":
    print get_real_ip()