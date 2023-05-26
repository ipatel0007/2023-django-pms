from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth.views import LoginView,LogoutView
from user.urls import *
urlpatterns = [
    path('create/',StocksCreateView.as_view(),name='stockscreate'),
    path('list/',StocksListView.as_view(),name='stockslist'),
    path('delete/<int:pk>',StockDeleteView.as_view(),name='stocksdelete'),
    path('update/<int:pk>',StockUpdateView.as_view(),name='stocksupdate'),
    path('pcreate/',PortfolioCreateView.as_view(),name='portfoliocreate'),
    path('pupdate/<int:pk>',PortfolioUpdateView.as_view(),name='portfolioupdate'),
    path('pdetails/<int:pk>',PortfolioDetailView.as_view(),name='portfoliodetail'),
    path('pdelete/<int:pk>/', PortfolioDeleteView.as_view(), name='portfoliodelete'),
    path('advise/', AdviseListView.as_view(), name='advise-list'),
    
]

   
    # path('delete/<int:pk>',StudentDeleteView.as_view(),name='studentdelete'),
    # path('update/<int:pk>',StudentUpdateView.as_view(),name='studentupdate'),
    # path('detail/<int:pk>',StudentDetailView.as_view(),name='studentdetail'),
    # path('addfile/',AddFileView.as_view(),name='addfile'),
    # path('filelist/',FileListView.as_view(),name='filelist'),