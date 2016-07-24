# -*- coding: utf-8 -*-

import requests
import time
import re
import shutil
import pyqrcode
import qrtools
import os
import random
import traceback

QR_URL = 'https://login.web.wechat.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fweb.wechat.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_='
QR_BASE = 'https://login.weixin.qq.com/qrcode/'
LOGIN_URL = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?uuid=%s&tip=1&_=%s'
COOKIE = 'webwxuvid=%s; wxuin=%s; wxsid=%s; wxloadtime=%s; webwx_data_ticket=%s; mm_lang=zh_CN; MM_WX_NOTIFY_STATE=1; MM_WX_SOUND_STATE=1'
DEFAULT_BASEURL = 'https://wx.qq.com/cgi-bin/mmwebwx-bin'
CONFIG_FILE = './node_modules/hubot-weixin/config.yaml'

def getQRURL():
    result = requests.get(QR_URL + str(int(time.time()))).text
    p = re.compile(r'.*window.QRLogin.uuid = "(.*)";')
    m = p.search(result)
    if m:
        return m.groups()[0]

def download(url, name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def qrDecode(url):
    qr = qrtools.QR()
    qr.decode(url)
    qr = pyqrcode.create(qr.data)
    return qr.terminal(quiet_zone=2)

def login(qr):
    result = requests.get(LOGIN_URL%(qr, str(int(time.time())))).text
    p = re.compile(r'.*redirect_uri="(.*)";')
    m = p.search(result)
    if m:
        return m.groups()[0]

def userinfo(string):
    p = re.compile(r'.*<skey>(.*)</skey>.*')
    m = p.search(string)
    if m:
        skey = m.groups()[0]
    else:
        skey = ''

    p = re.compile(r'.*<wxsid>(.*)</wxsid>.*')
    m = p.search(string)
    if m:
        sid = m.groups()[0]
    else:
        sid = ''

    p = re.compile(r'.*<wxuin>(.*)</wxuin>.*')
    m = p.search(string)
    if m:
        uin = m.groups()[0]
    else:
        uin = ''

    device_id = 'e' + ''.join([str(random.randint(0, 9)) for _ in range(15)])

    p = re.compile(r'.*webwx_data_ticket=([^;]+).*')
    m = p.search(string)
    if m:
        webwx_data_ticket = m.groups()[0]
    else:
        webwx_data_ticket = ''

    p = re.compile(r'.*webwxuvid=([^;]+).*')
    m = p.search(string)
    if m:
        webwxuvid = m.groups()[0]
    else:
        webwxuvid = ''

    p = re.compile(r'.*wxloadtime=([^;]+).*')
    m = p.search(string)
    if m:
        wxloadtime = m.groups()[0]
    else:
        wxloadtime = ''

    cookie = COOKIE % (webwxuvid, uin, sid, wxloadtime, webwx_data_ticket)
    return skey, sid, uin, device_id, cookie

def replace_file(src, baseurl, skey, sid, uin, device_id, cookie):
    try:
        context = ''
        read_file = open(src, 'r')
        for line in read_file.readlines():
            if line.startswith('DeviceID:'):
                line = 'DeviceID: "%s"\n' % device_id
            elif line.startswith('Sid:'):
                line = 'Sid: "%s"\n' % sid
            elif line.startswith('Skey:'):
                line = 'Skey: "%s"\n' % skey
            elif line.startswith('Uin:'):
                line = 'Uin: "%s"\n' % uin
            elif line.startswith('cookie:'):
                line = 'cookie: "%s"\n' % cookie
            elif line.startswith('baseUrl:'):
                line = 'baseUrl: "%s"\n' % baseurl
            context += line
        read_file.close()
        file = open(src, 'w')
        file.write(context)
        file.close()
    except:
        traceback.print_exc()
        print 'can not replace %s.' % CONFIG_FILE

if __name__ == '__main__':
    print "Get login qr image..."
    qr = getQRURL()
    if not qr:
        print 'can not get qr code'
        exit(1)
    qr_url = '%s%s' % (QR_BASE, qr)
    print "Download qr image...."
    download(qr_url, './qr_code.jpeg')

    print "Reproduce qr in terminal..."
    print qrDecode('./qr_code.jpeg')
    print 'Scan qr code or %s in 20 secends' % qr_url

    redirect_url = ''
    while 1:
        redirect_url = login(qr)
        if redirect_url:
            break
        else:
            time.sleep(2)
            print 'Try again...'

    p = re.compile(r'(.*mmwebwx-bin).*')
    m = p.search(redirect_url)
    if m:
        baseurl = m.groups()[0]
    else:
        baseurl = DEFAULT_BASEURL
    print 'baseurl', baseurl

    result = os.popen('curl -i "%s" 2>/dev/null' % redirect_url).read()
    skey, sid, uin, device_id, cookie = userinfo(result)
    print 'skey', skey
    print 'sid', sid
    print 'uin', uin
    print 'deviceid', device_id
    print 'cookie', cookie

    print 'Reconfig %s...' % CONFIG_FILE
    replace_file(CONFIG_FILE, baseurl, skey, sid, uin, device_id, cookie)

    print 'Start hubot -a weixin...'
    os.system('./bin/hubot -a weixin')
