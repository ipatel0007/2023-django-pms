from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
 
 path('euserreg/',EuserRegisterView.as_view(),name='euserreg'),
 path('advisorreg/',AdvisorRegisterView.as_view(),name='advisorreg'),
 path('login/',UserLoginView.as_view(),name='login'),
#  path('logout/',LogoutView.as_view(),name='logout'),
 path('euserdash/',my_view,name='euserdash'),
 path('logout/',LogoutView.as_view(template_name='user/logout.html',next_page=None),name = 'logout'),
#  path('loginView/',login_view,name='loginview')
 
]