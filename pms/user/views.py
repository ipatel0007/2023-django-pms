# Create your views here.
from urllib import response
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView
from .models import User
from .forms import EuserRegisterForm,AdvisorRegisterForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.core.mail import send_mail
from stocks.models import *
from stocks.views import StocksListView
# from django.db import transaction
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from stocks.models import Stocks,Sector
from .forms import *

# Create your views here.
class EuserRegisterView(CreateView):
    model = User
    form_class = EuserRegisterForm
    template_name = 'user/euser_register.html'
    success_url = "/user/login"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_euser = True
        user.save()
        
        send_mail(
            'Welcome to Grownited',
            'Dear {},\n\nWelcome to My Website! We are thrilled to have you as a new User.\n\nBest regards,\nMy Website Team'.format(user.username),
            'patelap871@gmail.com',
            [user.email],
            fail_silently=False,
        )
        
        return redirect('/user/login')
    
class AdvisorRegisterView(CreateView):
    model = User
    form_class = AdvisorRegisterForm
    template_name = 'user/advisor_register.html'
    success_url = "/user/login"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_advisor = True
        user.save()
        return super().form_valid(form)
    
class UserLoginView(LoginView):
     template_name = 'user/login.html'
    
    
     def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_euser:
                return '/user/euserdash'
            else:
                return render("no access")


# class EuserDashboardView(ListView):
#     def get(self, request, *args, **kwargs):
#         sectors = Sector.objects.all().values()
#         stocks = Stocks.objects.all().values()
        
#         return render(request, 'user/euser_dashboard.html',{
#             'sectors':sectors,
#             'stocks':stocks,
            
#         })

def my_view(request):
    stocks = Stocks.objects.all()
    sectors = Sector.objects.all()
    context = {'stocks': stocks, 'sectors': sectors}

    return render(request, 'user/euser_dashboard.html', context)




    

# class EuserDashView(ListView):
#     model = Stocks
#     template_name = 'user/euser_dashboard.html'
#     context_object_name = 'stockslist'
    
#     def get_queryset(self):
#         return super().get_queryset().filter(Stocks_id=self.kwargs['stocks_id']) 

# class UserStocksList(TemplateView):
#     template_name = 'user/euser_dashboard.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['stocks_stockslist'] = StocksListView.as_view()(self.request).context_data['stockslist']
#         return context


# def sendMail(request):
#     subject = "welcome to django"
#     message = "hello django"
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = ['apurvgarg66@gmail.com','vrajshah1930@gmail.com']
#     res = send_mail(subject,message,email_from,recipient_list)
#     if res>0:
#         print("mail sent")
#     else:
#         print("mail not sent")    
#     print(res)
#     return HttpResponse("mail sent")
    


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # Redirect to a success page.
#             return redirect('user/euser_dashboard.html')
#         else:
#             # Return an error message to the login form.
#             print("Error")
#             return render(request, 'user/login.html', {'error': 'Invalid username or password.'})
#     else:
#         # Display the login form.
#         print("OUTError")
#         return render(request, 'user/login.html')