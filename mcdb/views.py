from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
import mcdb.config as CONFIG
import json
import requests
from mcdb.models import *
from django.utils import timezone
import datetime

# Create your views here.

def main(request):
    return render(request, "index.html")


def index(request):
    return render(request, "index.html")


def test(request):
    return render(request, "test.html")


def r_oauth(request):
    """
    用户同意授权，获取code
    :param request:
    :return:
    """
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope={2}&state={3}#wechat_redirect"
    # redirect_uri = CONFIG.redirect_uri
    # #redirect_uri = urllib.parse.quote(redirect_uri)
    url.format(CONFIG.app_id, CONFIG.redirect2userUri, CONFIG.scope, CONFIG.state)
    # return redirect(url.format(CONFIG.app_id, redirect_uri, CONFIG.scope, CONFIG.state))
    #url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx42290aa31253c620&redirect_uri=http://zhzhang1997.natapp1.cc/user&response_type=code&scope=snsapi_userinfo&state=123&connect_redirect=1#wechat_redirect"
    return redirect(url)


def user(request):
    # # 判断access_token中是否存在access_token, 如果不存在，则回调 r_oauth 函数
    # is_exist = request.session.get('code', False)
    # if not is_exist:
    #     # return redirect(reverse('r_oauth'))
    # else:
    #
    code = request.GET.get("code")
    if not code:    # 如果没有获取到code
        print("Do not get code")
        return redirect(CONFIG.r_oauth)

    token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
    token_url = token_url.format(CONFIG.app_id, CONFIG.app_secret, code)
    data = requests.get(token_url)
    if not data:
        print("Do not have data")
        return HttpResponse("not find data!")
    data = json.loads(data.content.decode("utf-8"))
    if "errcode" in data:
        return redirect(CONFIG.r_oauth)

    access_token = data["access_token"]
    open_id = data["openid"]
    request.session['openid'] = open_id         # 将用户的openid存入session
    refresh_token = data["refresh_token"]

    if not access_token or not open_id:
        return None     # 判别access_token和open_id是否为空

    user_url = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN"
    user_info = requests.get(user_url.format(access_token, open_id))
    user_info = user_info.content.decode("utf-8")
    if not user_info:
        return None
    user_info = json.loads(user_info)

    # 解决token过期的问题
    if "errcode" in user_info and user_info["errcode"] == 40001:
        refresh_token_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={0}&grant_type=refresh_token&refresh_token={1}"
        refresh_token_url = refresh_token_url.format(CONFIG.app_id, refresh_token)
        r_userinfo = requests.get(refresh_token_url)
        r_userinfo = json.loads(r_userinfo.content.decode("utf-8"))
        access_token = r_userinfo['access_token']

    user_info = requests.get(user_url.format(access_token, open_id))
    user_info = user_info.content.decode("utf-8")
    user_info = json.loads(user_info)

    response = HttpResponse(json.dumps(user_info))
    response.set_cookie("userinfo", json.dumps(user_info), max_age=7 * 24 * 3600)   # 用户信息保存到cookie，设置过期时间为7天

    request.session['nickname'] = user_info.get('nickname')
    request.session['headimgurl'] = user_info.get('headimgurl')

    stu = Student()
    q_user = Student.objects.filter(openid=open_id)
    address = Address.objects.get(id=1)

    if len(q_user) == 0:
        stu.openid = open_id
        stu.name = user_info.get('nickname')
        # print(user_info.get('sex'))
        stu.gender = user_info.get('sex')
        stu.belong = address
        stu.save()

    else:
        stu = Student.objects.get(openid=open_id)
        stu.gender = user_info.get('sex')
        stu.belong = address
        stu.save()

    return render(request, 'index.html', {'index':CONFIG.HTML_INDEX['index']})


###################################################################
#   个人信息
###################################################################
def myinfo(request):
    nickname = request.session.get('nickname')
    headimgurl = request.session.get('headimgurl')
    result = {'nickname': nickname, 'headimgurl': headimgurl,'index':CONFIG.HTML_INDEX['myinfo']}
    return render(request, "myinfo.html", result)


###################################################################
#   展示全部课程
###################################################################
def lessons(request):
    openid = request.session.get('openid')  # 从session中获取openid
    student = Student.objects.get(openid=openid)  # 根据openid从数据库中获取对应学生对象
    mylesson = Course.objects.filter(students__openid=student.openid)
    mylessonID = []
    for lesson in mylesson:
        mylessonID.append(lesson.id)

    courses = Course.objects.all()
    result = {}
    for i, course in enumerate(courses):
        stri = '%d' % i
        course=course.to_dict()
        course.update({'tag':0})
        for myid in mylessonID:
            if myid == course['id']:
                course['tag']=1
        result.update({stri: course})

    return render(request, "lessons.html", {'result': result,'index':CONFIG.HTML_INDEX['lessons']})


###################################################################
#   展示我的已订阅课程
###################################################################
def mylessons(request):
    openid = request.session.get('openid')              # 从session中获取openid
    student = Student.objects.get(openid=openid)        # 根据openid从数据库中获取对应学生对象
    mylesson = Course.objects.filter(students__openid=student.openid)
    result = {}
    for i, lesson in enumerate(mylesson):
        stri = '%d' % i
        result.update({stri: lesson.to_dict()})
    return render(request, "mylessons.html", {'result': result,'index':CONFIG.HTML_INDEX['mylessons']})


###################################################################
#   订阅课程
###################################################################
def subscribe(request):
    course_id = request.POST.get('course_id')
    courseR = Course.objects.get(id=course_id)          # 这是要预定的课程
    openid = request.session.get('openid')
    student = Student.objects.get(openid=openid)

    mylesson = Course.objects.filter(students__openid=student.openid)
    mylessonID = []
    for lesson in mylesson:
        mylessonID.append(lesson.id)

    courses = Course.objects.all()
    result = {}
    for i, course in enumerate(courses):
        stri = '%d' % i
        course = course.to_dict()
        course.update({'tag': 0})
        for myid in mylessonID:
            if myid == course['id']:
                course['tag'] = 1
        result.update({stri: course})

    # 判断是否为会员
    isvip = VIP2Student.objects.filter(student__openid=student.openid)
    if len(isvip) == 0:
        return render(request, "lessons.html", {'warning': "对不起,你还不是本课程的会员", 'result': result, 'course_id': courseR.id,'index':CONFIG.HTML_INDEX['lessons']})

    # 判断会员是否过期
    vipdate = VIP2Student.objects.get(student__openid=student.openid)
    vip_end_time = vipdate.end_time             # 会员结束时间
    if vip_end_time < timezone.now().date():
        return render(request, "lessons.html", {'warning': "对不起，你的会员已经过期", 'result': result, 'course_id': courseR.id,'index':CONFIG.HTML_INDEX['lessons']})

    # 判断当前选课人数是否超过最大人数
    if courseR.current_number >= courseR.max_number:
        return render(request, "lessons.html", {'warning': "对不起，当前课程已满额", 'result': result, 'course_id': courseR.id,'index':CONFIG.HTML_INDEX['lessons']})

    courseR.current_number += 1
    courseR.save()

    course2student = Course2Student()
    course2student.student = student
    course2student.course = courseR
    course2student.save()
    url = CONFIG.lessons
    return redirect(url,{'result': result,'index':CONFIG.HTML_INDEX['lessons']})


###################################################################
#   取消订阅
###################################################################
def cancelSubscribe(request):
    course_id = request.POST.get('course_id')
    courseR = Course.objects.get(id=course_id)
    openid = request.session.get('openid')
    student = Student.objects.get(openid=openid)

    # 根据 openid 获取我的订阅课程
    mylesson = Course.objects.filter(students__openid=student.openid)
    result = {}
    for i, lesson in enumerate(mylesson):
        stri = '%d' % i
        result.update({stri: lesson.to_dict()})

    if courseR.date.date() - datetime.timedelta(days=1) < timezone.now().date():
        return render(request, "mylessons.html", {'warning': "距离开课前一天不能取消", 'result': result, 'course_id': courseR.id,'index':CONFIG.HTML_INDEX['mylessons']})

    # 取消预约，则课程的当前选课人数减一
    courseR.current_number -= 1
    courseR.save()
    # 从数据库中删除取消订阅的课程学生联系
    course2student = Course2Student.objects.get(course=courseR, student=student)
    course2student.delete()

    url = CONFIG.mylessons
    return redirect(url,{'index':CONFIG.HTML_INDEX['mylessons']})


