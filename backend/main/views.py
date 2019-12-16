from django.shortcuts import render
from django.http import JsonResponse
from . import models
import random
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import datetime
import base64
import hashlib
from . import recognition,heat
from django.core.files import File
from io import BytesIO
from urllib.request import urlopen
import os
import re

import warnings


def md5(string):
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(string.encode(encoding='utf-8'))    # 此处必须声明encode
    return(hl.hexdigest())

def get_date(time_stamp):
    try:
        time_stamp = int(time_stamp) / 1000
        dateArray = datetime.datetime.utcfromtimestamp(time_stamp)
        otherStyleTime = dateArray.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return otherStyleTime
    except Exception as e:
        return 'date over flow'

def invalid_time(time):
    if len(time)==0:
        return True
    else:
        try:
            time = int(time)
            return False
        except Exception as e:
            return True

# 编写装饰器检查用户是否登录
def check_login(func):
    def inner(request, *args, **kwargs):
        # 假设设置的cookie的key为login，value为yes
        if "session_id" in request.COOKIES.keys() and request.COOKIES["session_id"] != "":
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({"error":"please login"})
    return inner


@csrf_exempt
@check_login
def uploadUrl(request): # 图片上传函数
    warnings.filterwarnings('ignore')
    try:
        if request.method == 'POST':
            #print(type(request.POST.get ('url')))  # 打印出request的header详细信息
            url = request.POST.get ('url')
            r = urlopen(url)
            io = BytesIO(r.read())
            img = models.Img (raw_url=request.FILES.get ('url'))
            img.raw_url.save(("dl.jpg"), File(io))
            current_user = request.COOKIES["current_user"]
            img.username = current_user
            img.save()

            raw_path = str(img.raw_url)
            img.cook1_url = 'static/img/cook1/' + os.path.basename(raw_path)
            img.cook2_url = 'static/img/cook2/' + os.path.basename(raw_path)
            img.save()

            return JsonResponse({"raw_path": raw_path})
    except Exception as e:
        return JsonResponse({"error": "upload error"})

@csrf_exempt
@check_login
def uploadImg(request): # 图片上传函数
    warnings.filterwarnings('ignore')
    if request.method == 'POST':
        current_user = request.COOKIES["current_user"]
        img = models.Img (raw_url=request.FILES.get ('img'))
        img.username = current_user
        img.save()

        raw_path = str(img.raw_url)
        img.cook1_url = 'static/img/cook1/' + os.path.basename(raw_path)
        img.cook2_url = 'static/img/cook2/' + os.path.basename(raw_path)
        img.save()

        return JsonResponse({"raw_path": raw_path})
    return JsonResponse({"error": "upload error"})


@csrf_exempt
@check_login
def cook1(request):
    try:
        raw_path = request.POST.get('raw_path')
        cook1 = recognition.recognition(raw_path)
        return JsonResponse({"cook1_path": cook1})
    except Exception as e:
        return JsonResponse({"error": "cook1 failed"})


@csrf_exempt
@check_login
def cook2(request):
    try:
        raw_path = request.POST.get('raw_path')
        cook2 = heat.heat(raw_path)
        return JsonResponse({"cook2_path": cook2})
    except Exception as e:
        return JsonResponse({"error": "cook2 failed"})

@csrf_exempt
def login(request):
    data = {}
    if "session_id" in request.COOKIES.keys() and request.COOKIES["session_id"] != "":
        return JsonResponse({"error": "has logged in"})
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username:
                return JsonResponse({"error": "no such a user"})
            else:
                if password:  # 确保用户名和密码都不为空
                    try:
                        user = models.User.objects.get(username=username)
                    except:
                        return JsonResponse({"error":"no such a user"})

                    pwd_base64 = base64.b64encode(password.encode('utf-8'))
                    if user.password == pwd_base64.decode("utf-8"):
                        suffix = str(random.randint(1000000, 9999999))
                        session_id = md5(username+suffix)
                        user.save()
                        data["user"] = username
                        response = JsonResponse(data)
                        response.set_cookie("session_id",session_id)
                        response.set_cookie("current_user",username)
                        return response
                    else:
                        return JsonResponse({"error":"password is wrong"})
                else:
                    return JsonResponse({"error": "password is wrong"})
        else:
            return JsonResponse({"error": "require POST"})


@csrf_exempt
def logout(request):
    response = {}
    if request.method == 'POST':
        cookies = request.COOKIES
        if 'session_id' in cookies.keys() and cookies["session_id"]!='':
            try:
                response['user'] = request.COOKIES["current_user"]
                response = JsonResponse(response)
                response.delete_cookie('current_user')
                response.delete_cookie('session_id')
                return response
            except Exception as e:
                response['error'] = "no valid session"
        else:
            response['error'] = "no valid session"
    else:
        response['error'] = 'require POST'
    return JsonResponse(response)


@csrf_exempt
def logon(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if (not username) or (not password) :
            return JsonResponse({"error": "invalid parameters"})
        elif username == "admin":
            return JsonResponse({"error": "reserverd admin account"})
        else:
            try:
                tmp = models.User.objects.get(username=username)
                return JsonResponse({"error": "user exists"})
            except models.User.DoesNotExist:
                pwd_base64 = base64.b64encode(password.encode('utf-8'))
                user = models.User(username=username, password=pwd_base64.decode("utf-8"))
                user.save()
                return JsonResponse({"user": username})
    else:
        return JsonResponse({"error": "require POST"})


@csrf_exempt
@check_login
def delete_all(request):
    ids = request.POST.get('ids').split(',')
    for id in ids:
        try:
            img_id = int(id)

        except Exception as e:
            print(1,e)
            return JsonResponse({"error": "invalid parameters"})

        current_user = request.COOKIES["current_user"]
        if current_user == "admin":
            try:
                img = models.Img.objects.filter(img_id=img_id)[0]
                os.remove(str(img.raw_url))
                os.remove(str(img.cook1_url))
                os.remove(str(img.cook2_url))
                img.delete()
            except Exception as e:
                print(2,e)
                return JsonResponse({"error": "unknown img"})
        else:
            try:
                img = models.Img.objects.filter(img_id=img_id)[0]
                if(img.username != current_user):
                    return JsonResponse({"error": "unknown img"})
                else:
                    os.remove(str(img.raw_url))
                    os.remove(str(img.cook1_url))
                    os.remove(str(img.cook2_url))
                    img.delete()
            except Exception as e:
                print(3,e)
                return JsonResponse({"error": "unknown img"})
    return JsonResponse({"succes": "delete all"})


@csrf_exempt
@check_login
def img_delete(request):
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            img_id = int(id)
        except Exception as e:
            return JsonResponse({"error": "invalid parameters"})

        current_user = request.COOKIES["current_user"]
        if current_user == "admin":
            try:
                img = models.Img.objects.filter(img_id=img_id)[0]
                os.remove(str(img.raw_url))
                os.remove(str(img.cook1_url))
                os.remove(str(img.cook2_url))
                img.delete()
                return JsonResponse({"img_id": id})
            except Exception as e:
                print(e)
                return JsonResponse({"error": "unknown img"})
        else:
            try:
                img = models.Img.objects.filter(img_id=img_id)[0]
                if(img.username != current_user):
                    return JsonResponse({"error": "unknown img"})
                else:
                    os.remove(str(img.raw_url))
                    os.remove(str(img.cook1_url))
                    os.remove(str(img.cook2_url))
                    img.delete()
                    return JsonResponse({"img_id": id})
            except Exception as e:
                print(e)
                return JsonResponse({"error": "unknown img"})
    else:
        return JsonResponse({"error": "require POST"})


@csrf_exempt
@check_login
def admin_query(request):
    username = request.POST.get('username')
    current_user = request.COOKIES["current_user"]
    if current_user == "admin":
        if username:
            img = models.Img.objects.filter(username=username)
            q_list = []
            for e in img:
                tmp = {}
                tmp['img_id'] = e.img_id
                tmp['name'] = e.username
                tmp['time'] = str(e.c_time)[:-7]
                tmp['raw_url'] = str(e.raw_url)
                tmp['cook1_url'] = str(e.cook1_url)
                tmp['cook2_url'] = str(e.cook2_url)

                q_list.append(tmp)
            return JsonResponse({"list": q_list})
        else:
            img = models.Img.objects.filter(~Q(username=''))
            q_list = []
            for e in img:
                tmp = {}
                tmp['img_id'] = e.img_id
                tmp['name'] = e.username
                tmp['time'] = str(e.c_time)[:-7]
                tmp['raw_url'] = str(e.raw_url)
                tmp['cook1_url'] = str(e.cook1_url)
                tmp['cook2_url'] = str(e.cook2_url)
                q_list.append(tmp)
            return JsonResponse({"list": q_list})
    else:
        return JsonResponse({"error": "you are not admin"})


@csrf_exempt
@check_login
def user_query(request):
    current_user = request.COOKIES["current_user"]
    if current_user == "admin":
        img = models.Img.objects.filter(~Q(username=''))
        q_list = []
        for e in img:
            tmp = {}
            tmp['img_id'] = e.img_id
            tmp['name'] = e.username
            tmp['time'] = str(e.c_time)[:-7]
            tmp['raw_url'] = str(e.raw_url)
            tmp['cook1_url'] = str(e.cook1_url)
            tmp['cook2_url'] = str(e.cook2_url)

            q_list.append(tmp)
        return JsonResponse({"list": q_list})
    else:
        img = models.Img.objects.filter(Q(username=current_user))
        q_list = []
        for e in img:
            tmp = {}
            tmp['img_id'] = e.img_id
            tmp['name'] = e.username
            tmp['time'] = str(e.c_time)[:-7]
            tmp['raw_url'] = str(e.raw_url)
            tmp['cook1_url'] = str(e.cook1_url)
            tmp['cook2_url'] = str(e.cook2_url)
            q_list.append(tmp)
        return JsonResponse({"list": q_list})


def index(request):
    usr = request.COOKIES.get("current_user", None)
    return render(request, "index.html", {
        "is_login": "false" if usr is None else "true" ,
        "username": "" if usr is None else usr,
        "is_admin": "false" if usr != "admin" else "true"
    })