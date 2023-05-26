# Create your views here.
from typing import Any
from urllib import request, response
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from user.decoraters import advisor_required
from .models import EnrollmentRequest, User
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
from stocks.models import Stocks,Sector,UserPortfolioStock,Portfolio
from .forms import *
from django.contrib.auth.decorators import login_required
from user.decoraters import euser_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.views.generic import FormView
# from .models import EnrollmentRequest

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



@method_decorator(advisor_required(login_url='/user/login'), name='dispatch')
class AdvisorDashboard(ListView):
    #model = EnrollmentRequest
    template_name = 'user/advisor/index-analytics.html'
    context_object_name = 'enrollments'

    def get(self,request,*args,**kwargs):
        #userName = User.objects.filter(id=self.kwargs['pk']).values_list('username', flat=True).get()
        print(request.user.id)
        enroledUSer = EnrollmentRequest.objects.filter(advisor_id=request.user.id).values('user_id__id','user_id__username','user_id__email','user_id__phone_no','user_id__address','user_id__annual_income','status','created_at','updated_at')
        # print(enroledUSer)
        
        #print(userName)
        return render(request, 'user/advisor/index-analytics.html', {'enrollments':enroledUSer})

    def get_queryset(self):
        enrollments = EnrollmentRequest.objects.filter(advisor=self.request.user)
        for enrollment in enrollments:
            username = enrollment.user.username
            print(enrollment.id)
        # do something with the username
        return enrollments

class UserLoginView(LoginView):
     template_name = 'user/login.html'
    
    
     def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_euser:
                return '/user/euserdash'
            else:
                return '/user/advisor-dashboard'

class UserLogoutView(TemplateView):
    template_name = 'user/logout.html'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login'))

 

@method_decorator(euser_required(login_url='/user/login'), name='dispatch')
class MyView(TemplateView):
    template_name = 'user/euser_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ups = UserPortfolioStock.objects.all().filter(user=self.request.user)
        portfolio = Portfolio.objects.all().filter(user=self.request.user)
        sectors = Sector.objects.all()
        stocks = Stocks.objects.all()

        price_sort = self.request.GET.get('price_sort')
        if price_sort == 'asc':
            ups = ups.order_by('currentPrice')
        elif price_sort == 'desc':
            ups = ups.order_by('-currentPrice')

        labels = []
        data = []
        for p in portfolio:
            labels.append(p.portfolioName)
            # retrieve the portfolioScore value for the current portfolio name
            score = Portfolio.objects.filter(user=self.request.user, portfolioName=p.portfolioName).values_list('portfolioScore', flat=True).first()
            data.append(score)

        context.update({'ups': ups, 'portfolio': portfolio, 'sectors': sectors, 'stocks': stocks, 'labels': labels, 'data': data})
        
        return context




@method_decorator(euser_required(login_url='/user/login'), name='dispatch')
class AdvisorListView(ListView):
    model = User
    template_name = 'user/advisor_list.html'
    context_object_name = 'advisors'

    def get_queryset(self):
    # Filter the queryset to only include users with the 'advisor' role.
        advisors = User.objects.filter(is_advisor=True)
        enrollments = []
        for advisor in advisors:
            enrollment = EnrollmentRequest.objects.filter(advisor=advisor, user_id=self.request.user.id).values('id','user_id__id','user_id__username','user_id__email','user_id__phone_no','user_id__address','user_id__annual_income','status','created_at','updated_at')
            enrollments.append(enrollment)
        return zip(advisors, enrollments)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = EnrollmentRequest.status_choices
        return context
        
    

@method_decorator(euser_required(login_url='/user/login'), name='dispatch')
class EnrollmentRequestView(CreateView):
    model = EnrollmentRequest
    template_name = 'user/enrollment_request.html'
    form_class = EnrollmentRequestForm
    success_url = '/user/advisorlist'


    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        advisor_id = self.kwargs['advisor_id']
        initial['advisor'] = User.objects.get(id=advisor_id)
        # user_id = self.kwargs['user_id']
        # initial['usser'] = User.objects.get(id=user_id)
        return initial
    
    def form_valid(self, form):
        return super().form_valid(form) 


## Password reset functionality..............
class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        print("Send Mail-------------------------")
        context['email'] = to_email  # Add email to context
        super().send_mail(subject_template_name, email_template_name,
                            context, from_email, to_email, html_email_template_name)

class ForgotPasswordView(FormView):
    template_name = 'user/forgot_password.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        
        UserModel = get_user_model()
        print("email +",UserModel," "+email)
        try:
            user = UserModel.objects.get(email=email)
            print(user,"------  ")
        except UserModel.DoesNotExist:
            user = None

        if user:
            form.save(
                subject_template_name='user/password_reset_subject.txt',
                email_template_name='user/password_reset_email.html',
                html_email_template_name='user/password_reset_email.html',
                from_email=None,
                request=self.request,
                use_https=self.request.is_secure(),
                token_generator=default_token_generator,
                extra_email_context={'user': user},  # Pass User object to the extra_email_context
            )
        return super().form_valid(form) 


    

    
class UserDetailView(DetailView):
    model = User
    template_name = 'user/advisor/user_details.html'
    context_object_name = 'userdetails'

    def get_object(self, queryset=None):
        # Get the id of the selected user from the URL parameters
        user_id = self.kwargs['pk']
        # Get the User object with the specified id
        user = get_object_or_404(User, pk=user_id)
        # Return a queryset containing the User object
        return User.objects.filter(pk=user_id)

class UserStockDetailView(DetailView):
    model = Portfolio
    template_name = 'user/advisor/advisor_user_portfolios.html'
    context_object_name = 'userstockdetails'

    def get_object(self, queryset=None):
        # Get the id of the selected user from the URL parameters
        user_id = self.kwargs['pk']
        # Get the User object with the specified id
        user = get_object_or_404(User, pk=user_id)
        # Return a queryset containing the User object
        return Portfolio.objects.filter(user_id=user_id)
     


class AdvisorPortfolioDetailView(DetailView):
    model = UserPortfolioStock
    template_name = 'user/advisor/advisor_user_pdetails.html'
    context_object_name = 'portfoliodetails'

    
    def get_labels_and_data(self):
        labels = []
        data = []
        data1 = []
        data2 = []
        user_portfolio = UserPortfolioStock.objects.filter(portfolio=self.kwargs['pk'])
        stocks = Stocks.objects.filter(userportfoliostock__portfolio=self.kwargs['pk']).distinct()
        
        
        for stock in stocks:
            stock_name = stock.stockName
            stock_price = user_portfolio.filter(stocks=stock).values_list('currentPrice', flat=True).last()
            invest_price = user_portfolio.filter(stocks=stock).values_list('investPrice', flat=True).last()
            stock_invest_price = user_portfolio.filter(stocks=stock).values_list('investPrice', flat=True).last()
            if stock_price is not None:
                labels.append(stock_name)
                data.append(stock_price)
                data2.append(invest_price)
                if stock_invest_price is not None:
                    data1.append(stock_price - stock_invest_price)
                else:
                    data1.append(None)
        # print(data1)
        return labels, data, data1, data2


    def get(self, request, *args, **kwargs):
        labels, data, data1,data2 = self.get_labels_and_data()
        
        print(f"request.user = {request.user}")
        portfolio = Portfolio.objects.filter(userportfoliostock=self.kwargs['pk'],user=request.user).values()
        userporfolio = UserPortfolioStock.objects.filter(portfolio=self.kwargs['pk'])
        portfolioName = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('portfolioName', flat=True).get()
        pid = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('id', flat=True).get()
       
        if request.method == 'GET':
            price_sort = request.GET.get('price_sort')
            if price_sort == 'asc':
                userporfolio = userporfolio.order_by('currentPrice')
            elif price_sort == 'desc':
                userporfolio = userporfolio.order_by('-currentPrice')

        return render(request, self.template_name, {'portfoliodetails': self.get_object(),
                                                    'portfolio': portfolio,
                                                    'ups': userporfolio,
                                                    'portfolioName': portfolioName,
                                                    'pid': pid,
                                                    'labels': labels,
                                                    'data': data,
                                                    'data1': data1,
                                                    'data2': data2,
                                                    'label1': 'Price difference'})

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return redirect('portfoliodetail', pk=self.kwargs['pk'])


@method_decorator(advisor_required(login_url='/user/login'), name='dispatch')
class AdviseStockView(CreateView):
    model = Advise
    template_name = 'user/advisor/stockadvise.html'
    form_class = StockAdviseForm
    success_url = '/user/advisor-dashboard'

    
    
    
    def form_valid(self, form):
        return super().form_valid(form) 
    def get_initial(self):
        initial = super().get_initial()
        initial['adviser'] = self.request.user
        user_id = self.kwargs['user_id']
        initial['usser'] = User.objects.get(id=user_id)
        # user_id = self.kwargs['user_id']
        # initial['usser'] = User.objects.get(id=user_id)
        return initial
    
    
    
@method_decorator(advisor_required(login_url='/user/login'), name='dispatch')
class AdvisorUserListView(ListView):
    #model = EnrollmentRequest
    template_name = 'user/advisor/enrolledusers.html'
    context_object_name = 'enrollments'

    def get(self,request,*args,**kwargs):
        #userName = User.objects.filter(id=self.kwargs['pk']).values_list('username', flat=True).get()
        print(request.user.id)
        enroledUSer = EnrollmentRequest.objects.filter(advisor_id=request.user.id).values('id','user_id__id','user_id__username','user_id__email','user_id__phone_no','user_id__address','user_id__annual_income','status','created_at','updated_at')
        # print(enroledUSer)
        #print(userName)
        return render(request, 'user/advisor/enrolledusers.html', {'enrollments':enroledUSer})

    def get_queryset(self):
        enrollments = EnrollmentRequest.objects.filter(advisor=self.request.user)
        for enrollment in enrollments:
            username = enrollment.user.username
        # do something with the username
        return enrollments

class EnrollmentRequestUpdateView(UpdateView):
    model = EnrollmentRequest
    form_class = EnrollmentRequestUpdateForm
    template_name = 'user/advisor/enrollment_request_update.html'
    success_url = reverse_lazy('enrolledusers')

    def form_valid(self, form):
        enrollment_request = form.save(commit=False)
        enrollment_request.status = form.cleaned_data['status']
        enrollment_request.save()
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.object.user
        initial['advisor'] = self.request.user
        return initial

    def get_object(self):
        return get_object_or_404(EnrollmentRequest, pk=self.kwargs['pk'])
    
