# -*- coding: UTF-8 -*-

import requests
import hashlib
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import pytesseract
import os
import xmltodict
import json
import re
import base64

url = 'http://223.2.10.26/cas/logon.action'
url2 = 'http://223.2.10.26/cas/genValidateCode'
url3 = 'http://223.2.10.26/frame/jw/teacherstudentmenu.jsp?menucode=JW1314'
url4 = 'http://223.2.10.26/student/xscj.stuckcj.jsp?menucode=JW130706'
url5 = 'http://223.2.10.26/jw/common/showYearTerm.action'
url6 = 'http://223.2.10.26/student/xscj.stuckcj_data.jsp'

url7 = 'http://223.2.10.26/STU_BaseInfoAction.do?hidOption=InitData&menucode_current=JW13020101'
url8 = 'http://223.2.10.26/student/stu.xsxj.xjda.jbxx.html?menucode=JW13020101'

url9 = 'http://223.2.10.26/student/wsxk.xskcb10319.jsp'
url10 = 'http://223.2.10.26/student/xkjg.wdkb.jsp?menucode=JW130418'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

s = requests.Session()

# 登录
def login(username,password):
    while True:
        yzm = Verify()
        status = getStatus(username, password, yzm)
        if not status['status'] == '401':
            break
    r = dict(message=status['message'],status=status['status'])
    if status['status'] == '200':
        r.update(cookies={'JSESSIONID':s.cookies['JSESSIONID']})
    return json.dumps(r)

# 基本信息
def getInfo(cookies):
    w = requests.Session()
    w.headers.update({'Referer': url8})
    try:
        p = w.post(url7, headers=header,cookies=cookies)
        obj = xmltodict.parse(p.text)
        obj.update(status='200',message=u'基本信息')
    except:
        obj=dict(status='402',message=u'cookies已过期')
    return json.dumps(obj)

# 学业成绩
def getScore(cookies,sjxz=1,xn=2016,xq=0):
    w = requests.Session()
    p = w.post(url5, headers=header,cookies=cookies)
    userCode = p.json()['userCode']
    w.get(url3, headers=header,cookies=cookies)
    w.headers.update({'Referer': url3})
    w.get(url4, headers=header,cookies=cookies)

    data = {
        'sjxz': 'sjxz'+str(sjxz),
        'ysyx': 'yxcj',
        'userCode': userCode,
        'xn':str(xn),
        'xn1':str(int(xn)+1),
        'xq':xq,
        'ysyxS': 'on',
        'sjxzS': 'on',
        'menucode_current': ''
    }

    w.headers.update({'Referer': url4})
    f = w.post(url6, data, headers=header,cookies=cookies)
    # print (f.text)
    # print (re.findall(u'点击刷新验证码', f.text))
    if re.findall(u'没有检索到记录!', f.text):
        return json.dumps(dict(status='401',message=u'没有检索到记录!'))
    if re.findall(u'点击刷新验证码', f.text):
        return json.dumps(dict(status='402',message=u'cookies已过期'))
    soup = BeautifulSoup(f.text, 'html.parser')

    info = list()
    table = soup.find('div', group='group').find_all('div')
    for i in table:
        info.append(i.string.split(u'：')[1])
    result = dict(yx=info[0],xzbj=info[1],xh=info[2],xm=info[3],dysj=info[4])

    term = list()
    a = soup.find_all('td', style='border: none;width:25%;')
    for i in a:
        term.append(i.string.split(u'：')[1])
    #print (term)

    grade=list()
    #tempre=dict()
    num = 0
    tb = soup.find_all('table', style='clear:left;width:256mm;font-size:12px;')
    for i in tb:
        t = i.find('tbody').find_all('tr')
        termgrade=list()
        for j in t:
            g = j.find_all('td')
            temp = list()
            for k in g:
                temp.append(k.string)
            tempgrade=dict(xh=temp[0],kchj=temp[1],xf=temp[2],lb=temp[3],xdxz=temp[4],khfs=temp[5],cj=temp[6],hdxf=temp[7],jd=temp[8],xfjd=temp[9],bz=temp[10])
            termgrade.append(tempgrade)
            #print (termgrade)
            #grade.upgrade()
        #print (num)
        tempre=dict(xq=term[num],grade=termgrade)
        grade.append(tempre)
        num += 1
    result.update(allgrade=grade,status='200',message=u'学业成绩')
    return json.dumps(result)

# 我的课表
def getSchedule(cookies,xn=2016,xq=0):
    w = requests.Session()
    p = w.post(url5, headers=header,cookies=cookies)
    userCode = p.json()['userCode']
    tempstr = ('xn='+str(xn)+'&xq='+str(xq)+'&xh=201300002445').encode('UTF-8')
    #print (bytes(tempstr))
    w.headers.update({'Referer': url10})
    f=w.get(url9,params={'params':base64.b64encode(tempstr)},cookies=cookies)
    if re.findall(u'没有检索到记录!', f.text):
        return json.dumps(dict(status='401',message=u'没有检索到记录!'))
    if re.findall(u'点击刷新验证码', f.text):
        return json.dumps(dict(status='402',message=u'cookies已过期'))

    soup = BeautifulSoup(f.text, 'html.parser')

    table = soup.find_all('div',class_="div1")
    kcb = list()
    for i in table:
        li=list()
        temp=dict(rq=i['id'])
        for j in i.find('span').find('div').descendants:
            li.append(j)
        temp.update(kcm=li[0],ls=li[2].rstrip(),sksj=li[4])
        try:
            temp.update(skdd=li[6])
        except:
            temp.update(skdd=None)
        kcb.append(temp)
    return json.dumps(dict(status='200',message=u'我的课表',kcb=kcb))

def md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()

def getStatus(username, pwd, yzm):
    data = {
        'username': username,
        'password': md5(md5(pwd) + md5(yzm)),
        'randnumber': yzm,
        'isPasswordPolicy': '1'
    }
    t = s.post(url, data, headers=header)
    return t.json()

# 识别验证码
def Verify():
    try:
        r = s.get(url2, headers=header)
        buff = BytesIO(r.content)
        im = Image.open(buff)
        im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)
        im = im.convert('1')
        vcode = pytesseract.image_to_string(im, config='-psm 3')
    except:
        vcode = ''
    return vcode
