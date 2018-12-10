#! /usr/bin/env python
# -*- coding:utf8 -*-

import smtplib
from email.mime.text import MIMEText

#收件人(列表)
mailto_list=['shaobangjie@163.com']
#使用的邮箱的smtp服务器地址
mail_host="smtp.163.com"
#用户名          
mail_user="shaobangjie@163.com"
#密码                        
mail_pass="163Sbj203203"
#邮箱的后缀
#mail_postfix="postfix"

def send_mail(to_list,sub,content):

    #me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    me="hello"+"<"+mail_user+">"
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    #将收件人列表以‘；’分隔
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                            
        server.login(mail_user,mail_pass)               
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__=="__main__":
    if send_mail(mailto_list,"hello","haha!"):  #邮件主题和邮件内容
        print "done!"
    else:
        print "failed!"