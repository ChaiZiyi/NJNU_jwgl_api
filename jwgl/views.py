from django.shortcuts import render, redirect
from django.http import HttpResponse
from collections import OrderedDict
from . import apis
import json

def index(request):
    return render(request, 'index.html')

def info(request):
    if request.method == 'GET':
        cookies = request.COOKIES
        return HttpResponse(apis.getInfo(cookies))
    return HttpResponse(json.dumps(dict(status='404',message=u'你来到了没有数据的荒原')))

def login(request):
    if request.method == 'GET':
        username = request.GET.get('username','')
        password = request.GET.get('password','')
        result = apis.login(username,password)
        response = HttpResponse(result)
        try:
            response.set_cookie('JSESSIONID',json.loads(result)['cookies']['JSESSIONID'])
        except:
            pass
        return response
    return HttpResponse(json.dumps(dict(status='404',message=u'你来到了没有数据的荒原')))

def scores(request):
    if request.method == 'GET':
        cookies = request.COOKIES
        sjxz = request.GET.get('sjxz',1)
        xn = request.GET.get('xn',2016)
        xq = request.GET.get('xq',0)
        return HttpResponse(apis.getScore(cookies,sjxz,xn,xq))
    return HttpResponse(json.dumps(dict(status='404',message=u'你来到了没有数据的荒原')))

def schedule(request):
    if request.method == 'GET':
        cookies = request.COOKIES
        xn = request.GET.get('xn',2016)
        xq = request.GET.get('xq',0)
        return HttpResponse(apis.getSchedule(cookies,xn,xq))
    return HttpResponse(json.dumps(dict(status='404',message=u'你来到了没有数据的荒原')))

def others(request):
    return HttpResponse(json.dumps(dict(status='404',message=u'你来到了没有数据的荒原')))
