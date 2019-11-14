"""TDSport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

from mcdb import views
from werobot.contrib.django import make_view
from MyRobot.robot import myrobot
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),       # 后台管理页面
    url(r'^$', views.main),
    url(r'^r_oauth/', views.r_oauth),
    url(r'^user/', views.user),
    url(r'^test/', views.test),
    url(r'^robot/', make_view(myrobot)),
    url(r'^index/', views.index),
    url(r'^myinfo/', views.myinfo),
    url(r'^lessons/', views.lessons),
    url(r'^mylessons/', views.mylessons),
    url(r'^subscribe/', views.subscribe),
    url(r'^cancelSubscribe', views.cancelSubscribe),
    url(r'^MP_verify_sxRnPUEiNOoBK6Xf.txt', TemplateView.as_view(template_name='MP_verify_sxRnPUEiNOoBK6Xf.txt', content_type='text/plain')),
]
