# -*- coding:utf-8 -*-
import itchat
import email
import imaplib
from email.parser import Parser
from HTMLParser import HTMLParser

imapserver = "your imap and port"
username = "your username"
password = "your passwd"
itchat.auto_login(hotReload=True)
admin = itchat.search_friends(name=u'大叔')
admin = admin[0]['UserName']

def getMail():
    conn = imaplib.IMAP4(imapserver,143)
    conn.login(username, password)
    conn.select("INBOX")
    type, data = conn.search(None, 'ALL')
    msgList = data[0].split()
    type,data=conn.fetch(msgList[len(msgList)-1],'(RFC822)')
    msg=email.message_from_string(data[0][1])
    msg_content=msg.get_payload(decode=True)
    return msg_content

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.list = []
    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            for (variable, value) in attrs:
                if variable == 'style':
                    self.flag = True
    def handle_data(self,data):
        if self.flag:
            self.list.append(data)

def mailRun():
    getmail = getMail()
    parser = MyHTMLParser()
    parser.feed(getmail)
    mailtext = parser.list
    mailtext = ''.join(mailtext).replace("\t","").replace("\r\n","").replace(" ","")
    mailtext = mailtext.replace('事件概况','\n事件概况').replace('安全处置建议', '\n安全处置建议').replace('事件解释', '\n事件解释')
    return mailtext.decode('utf-8')

@itchat.msg_register(itchat.content.TEXT)
def group_text(msg):
    if u'报警邮件' in msg['Text']:
        itchat.send_msg(m, msg['FromUserName'])

if __name__ == "__main__":
    m = mailRun()
    itchat.run()
