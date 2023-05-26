from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('create/',StocksCreateView.as_view(),name='stockscreate'),
    path('list/',StocksListView.as_view(),name='stockslist'),
    path('delete/<int:pk>',StockDeleteView.as_view(),name='stocksdelete'),
    path('update/<int:pk>',StockUpdateView.as_view(),name='stocksupdate'),
 
 
]

   
    # path('delete/<int:pk>',StudentDeleteView.as_view(),name='studentdelete'),
    # path('update/<int:pk>',StudentUpdateView.as_view(),name='studentupdate'),
    # path('detail/<int:pk>',StudentDetailView.as_view(),name='studentdetail'),
    # path('addfile/',AddFileView.as_view(),name='addfile'),
    # path('filelist/',FileListView.as_view(),name='filelist'),