from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
 
 path('euserreg/',EuserRegisterView.as_view(),name='euserreg'),
 path('advisorreg/',AdvisorRegisterView.as_view(),name='advisorreg'),
 path('login/',UserLoginView.as_view(),name='login'),
 path('euserdash/',MyView.as_view(),name='euserdash'),
 path('logout/', UserLogoutView.as_view(), name='logout'),
 path('advisorlist/', AdvisorListView.as_view(), name='advisorlist'),
 path('advisor-dashboard/', AdvisorDashboard.as_view(), name='advisor_dashboard'),
 path('enroll-request/<int:advisor_id>/',EnrollmentRequestView.as_view() , name='enroll_request'),
#  path('enroll-request/',EnrollRequestView.as_view() , name='enroll_request'),
 path('userdetail/<int:pk>',UserDetailView.as_view(),name='userdetail'),
 path('userstockdetail/<int:pk>',UserStockDetailView.as_view(),name='userstockdetail'),
 path('apdetails/<int:pk>',AdvisorPortfolioDetailView.as_view(),name='apdetails'),
 path('stockadvise/<int:user_id>/',AdviseStockView.as_view(),name='stockadvise'),
 path('enrolledusers/',AdvisorUserListView.as_view(),name='enrolledusers'),
 path('enrollment_request/<int:pk>', EnrollmentRequestUpdateView.as_view(), name='enrollment_request_update'),

 
 path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
 path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
 path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
 path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
 path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
 
]

