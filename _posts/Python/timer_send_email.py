#!/usr/bin/env python

from threading import Timer
from real_ip import  get_real_ip
from send_email import send_email
import datetime
#import time  

timer_interval=60*60
def delayrun():
    #morning
    start = datetime.time(23,59,59)
    end = datetime.time(1)
    timestamp = datetime.datetime.now().time()
    if start <= timestamp <= end:
        ip = get_real_ip()
        send_email("shaobangjie@163.com",ip,"hi, the latest ip is :["+ip+"]")
    #arfternoon
    start = datetime.time(12)
    end = datetime.time(13)
    if start <= timestamp <= end:
        ip = get_real_ip()
        send_email("shaobangjie@163.com",ip,"hi, the latest ip is :["+ip+"]")

        
#while True:  
#    time.sleep(0.1)  
#    print 'main running'  

if __name__ == "__main__":
    t=Timer(timer_interval,delayrun)  
    t.start()  