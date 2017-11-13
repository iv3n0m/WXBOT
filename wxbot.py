#coding:utf-8
import os
import re
import shutil
import time
import sqlite3
import itchat
import json
import requests
from itchat.content import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

jianjie = {
    	u'大叔': u'大者大而无疆，叔者古往今来。所以大叔就是空间和时间，就是宇宙啊!',
        u'蜜儿': u'传说中的春秋第一网红美女，现客服大主管的38G大咪咪！',
        u'Coral': u'这位是sobug运营第一美女 36D的扣肉散姨！',
        u'若可': u'二进制萌妹子，精灵古怪的若可美少女！',
        u'正太': u'常年混土司，习科的大牛，乌云前核心，现在正在准备考研的开二代美少年一枚',
        u'九守': u'老九，安全运维大牛，乙方高级工程师，项目经理!',
        u'老骚': u'老骚，资深游戏测试大牛，密宗上师，专门给人灌肠的黄教弟子，以后要成为佛的男人!' ,
        u'手淫哥': u'传说中每秒300下的男人，拍黄片大神，东莞phper！',
        u'hehe': u'傲娇暴走小学生，安全大牛，传说中搞对象最多的小学生!', 
        u'可乐': u'批量渗透大吊，补天排名50的男人，专门搞批量日站，现在是乙方渗透大牛' ,
        u'R总': u'小Rpython技术大牛，itchat机器人大屌，安全牛，传说中比较低调的技术人员Django大神!',
        u'图南': u'CTO图南，安全圈最可爱的男人，机器人小图之父，传说中的程序员，每年赚的钱可以绕地球五百圈，经常被妹子撩的男人!',
        u'小黄文': u'官能作家小黄文，纯情的白莲花，sobug花魁妹妹!', 
        u'慕容复': u'指法碾压加藤鹰，口技名镇东南亚!', 
	u'老炮': u'SEO界大神，传说中的羊毛帝！',
	u'切糕': u'统御安全，运维，编程界的男人！',
	u'Rocky': u'运维上古大神，精通各种数据库，交换机，路由器，防火墙，各种大数据，各种编程语言，人工智能！'
}
a = jianjie.keys() 

msg_dict = {}
rev_tmp_dir = "/root/wxbot/file"
face_bug = None

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def getip(ip):
    site = 'http://ip.taobao.com//service/getIpInfo.php?ip=' + ip
    r = requests.get(site, headers=headers)
    rdata = r.json().get('data')
    code = r.json()['code']
    if code == 0:
        ipp = rdata['ip']
        city = rdata['city']
        isp = rdata['isp']
        rr = u'小黄人偷偷的告诉你IP:%s是来自%s的,运营商为%s' % (ipp,city,isp)    
    else:
        rr = u'你不要骗我，这个ip不存在的！'
    return rr


conn = sqlite3.connect('wx.db')
print 'good db!'
cur = conn.cursor()
#cur.execute("DROP TABLE SHENDUNJU ")
#cur.execute("CREATE TABLE SHENDUNJU (ID TEXT,NAME TEXT,TIME TEXT,MESSAGE TEXT);")

@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
#@itchat.msg_register(TEXT, isGroupChat=True)
def group_text(msg):
    global name
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg_time = msg['CreateTime']
    msg_content = msg['Content']
    msg_shar_url = None 
    content = msg['Text']
    name = content[5:]


    #print msg['MsgId'].encode('utf-8')
    #print msg['ActualUserName'].encode('utf-8')
    #print msg['CreateTime']
    #print type(msg['CreateTime'])
    #print msg['Content'].encode('utf-8')
    
    if msg['isAt'] and (name in jianjie.keys()):
        itchat.send_msg(jianjie[name], msg['FromUserName'])

    if msg['isAt'] and ('ip' in msg['Text']):
	ipa = msg['Text']
	ipa = re.findall(r'\d+.\d+.\d+.\d+', ipa)
	ip = ipa[0]
	itchat.send(getip(ip), msg['FromUserName'])
    
    while 1:
        all_msg = [
            msg['MsgId'].decode('utf-8'),
            msg['ActualUserName'].decode('utf-8'),
            msg['CreateTime'],
            msg['Content'].decode('utf-8')
		]
        cur.executemany("INSERT INTO SHENDUNJU VALUES (?,?,?,?)",all_msg)
        conn.commit()
    
    cur.execute('SELECT * FROM SHENDUNJU')
    print cur.fetchone()
    print cur.fetchall()

    mmm = msg['Content'].encode('utf-8')
    if u'撤回了一条消息' in msg['Content']:
        print 'HAHAHAHAH'
    else:
        with open('wx.txt', 'w') as f:
            f.write(mmm)
    
        with open('wx.txt', 'r') as f:
	    global lll
            lines = f.readlines()
            lll = lines[-1]
    aaa = u'被我看到了，你撤回的消息是:%s' % lll

    if msg['MsgType'] == 10002:
	aaa = cur.execute("SELECT MESSAGE FROM SHENDUNJU")
	itchat.send_msg(aaa, msg['FromUserName'])
	print type(msg)


    cur.close()
    conn.close()
itchat.auto_login(hotReload=True, enableCmdQR=2)
admin = itchat.search_friends(name=u'大叔')
admin = admin[0]['UserName']
if __name__ == "__main__":
    try:
        itchat.send(u'机器人上线!', toUserName=admin)
	itchat.run()
	itchat.send(u'机器人下线!', toUserName=admin)
    except KeyboardInterrupt:
	itchat.logout()
