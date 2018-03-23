"""MobAlarm URL Configuration

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
from django.contrib import admin
from appserver import views
urlpatterns = [
	url(r'^register/username=(?P<username>.*)&password=(?P<password>.*)',views.user_register, name = 'user_register'),
    url(r'^login/username=(?P<username>.*)&password=(?P<password>.*)',views.user_login, name = 'user_login'),
	url(r'^add/username=(?P<username>.*)&category=(?P<category>.*)', views.add_event, name = 'add_event'),
	url(r'^delete/username=(?P<username>.*)&category=(?P<category>.*)', views.delete_event, name = 'delete_event'),
	url(r'^location/username=(?P<username>.*)&latitude=(?P<latitude>[+-]?(\d*\.)?\d+)&longitude=(?P<longitude>[+-]?(\d*\.)?\d+)', views.handle_location, name = 'handle_location'),
	url(r'^processdata/password=(?P<password>.*)/category=(?P<category>.*)', views.process_data, name = 'process_data'),
    url(r'^admin/', admin.site.urls),
]
