"""Mserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from . import views 

urlpatterns = [
    url(r'^$',views.home,name='home' ),
    url(r'^getdata/$', views.getdata, name='getdata'),
    url(r'^analyze_nmon/$', views.analyze_nmon, name='analyze_nmon'),
    url(r'^nmon_2_img/$', views.nmon_2_img, name='nmon_2_img'),
    url(r'^nmon_2_host/$', views.nmon_2_host, name='nmon_2_host'),
    url(r'^nmon_2_start/$', views.nmon_2_start, name='nmon_2_start'),
    url(r'^put_nmon/$', views.put_nmon, name='put_nmon'),
    url(r'^start_all/$', views.start_all, name='start_all'),
    url(r'^add_server/$', views.add_server, name='add_server'),
    url(r'^nmon_2_img_many/$', views.nmon_2_img_many, name='nmon_2_img_many'),
    url(r'^many_2_imgs/$', views.many_2_imgs, name='many_2_imgs'),
    url(r'^run_cmd_many/$', views.run_cmd_many, name='run_cmd_many'),
]
