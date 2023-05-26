from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.views.generic import ListView,DetailView
from .forms import *
from django.contrib.auth.decorators import login_required
from user.decoraters import euser_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

from .models import *

@method_decorator([login_required(login_url='/user/login'),euser_required],name='dispatch')
class StocksListView(ListView):
    model = UserPortfolioStock
    template_name = 'stocks/liststocks.html'
    context_object_name = 'stockslist'

    def get_queryset(self):
        queryset = super().get_queryset()
        price_sort = self.request.GET.get('price_sort')
        if price_sort == 'asc':
            queryset = queryset.order_by('currentPrice')
        elif price_sort == 'desc':
            queryset = queryset.order_by('-currentPrice')
        return queryset

    

    




    

@method_decorator([login_required(login_url='/user/login'),euser_required],name='dispatch')
class StocksCreateView(CreateView):
    # fields = ('user','portfolio','stocks','qty','purchaseDate','investPrice','currentPrice')
    
    model = UserPortfolioStock
    form_class = StocksCreationForm
    template_name = 'stocks/createstock.html'
    # success_url = '/user/euserdash'
    
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['portfolio'] = Portfolio.objects.filter(user=self.request.user).values_list('id', flat=True)
    #     return initial

    def get_success_url(self):
        print(f"self.object.pk = {self.object.pk}")
        portfolio = self.object.portfolio
    
    # Get the id of the Portfolio object
        pid = portfolio.id
    
    # Use the id of the Portfolio object as the value for the pk argument
        return reverse('portfoliodetail', kwargs={'pk': pid})
    
    

    

@method_decorator([login_required(login_url='/user/login'),euser_required],name='dispatch')
class StockDeleteView(DeleteView):
    model = UserPortfolioStock
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    # success_url = '/user/euserdash/'
    def get_success_url(self):
        print(f"self.object.pk = {self.object.pk}")
        portfolio = self.object.portfolio
    
    # Get the id of the Portfolio object
        pid = portfolio.id
    
    # Use the id of the Portfolio object as the value for the pk argument
        return reverse('portfoliodetail', kwargs={'pk': pid})  

     


@method_decorator([login_required(login_url='/user/login'),euser_required],name='dispatch')
class StockUpdateView(UpdateView):
    model = UserPortfolioStock
    form_class = StocksUpdateForm
    template_name = 'stocks/updatestock.html'
    
    def get_success_url(self):
        print(f"self.object.pk = {self.object.pk}")
        portfolio = self.object.portfolio
    
    # Get the id of the Portfolio object
        pid = portfolio.id
    
    # Use the id of the Portfolio object as the value for the pk argument
        return reverse('portfoliodetail', kwargs={'pk': pid})

    
    # def get_success_url(self):
    #     return f'/stocks/pdetails/{self.object.pk}/'

@method_decorator([login_required(login_url='/user/login'),euser_required],name='dispatch')
class PortfolioCreateView(CreateView):
     
     form_class = PortfolioCreateForm
     template_name = 'stocks/createportfolio.html'
     success_url = '/user/euserdash'

     def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial


     

@method_decorator([login_required(login_url='/user/login'),euser_required],name='dispatch')
class PortfolioUpdateView(UpdateView):
    model = Portfolio
    fields = ('portfolioName',)
    template_name = 'stocks/createportfolio.html'
    success_url = '/user/euserdash/'


@method_decorator([login_required(login_url='/user/login'),euser_required],name='dispatch')
class PortfolioDeleteView(DeleteView):
    model = Portfolio
    success_url = reverse_lazy('euserdash')
    
    def get_object(self, queryset=None):
        """Hook to ensure object is owned by request.user."""
        obj = super(PortfolioDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj
    
   


@method_decorator([login_required(login_url='/user/login'), euser_required], name='dispatch')
class PortfolioDetailView(DetailView):
    model = UserPortfolioStock
    template_name = 'stocks/portfoliodetails.html'
    context_object_name = 'portfoliodetails'

    
    def get_labels_and_data(self):
        labels = []
        data = []
        data1 = []
        data2 = []
        profit_loss = []
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
                    profit_loss.append(stock_price - stock_invest_price)
                    data1.append(abs(stock_price - stock_invest_price))
                else:
                    profit_loss.append(None)
                    data1.append(None)
                print(data1)
        return labels, data, data1, data2, profit_loss



    def get(self, request, *args, **kwargs):
        labels, data, data1,data2, profit_loss = self.get_labels_and_data()
    
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
                                                'label1': 'Price difference',
                                                'profit_loss': profit_loss})

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return redirect('portfoliodetail', pk=self.kwargs['pk'])
        
    
class AdviseListView(ListView):
    model = Advise
    template_name = 'user/advised_stocks.html'
    context_object_name = 'advises'

    def get_queryset(self):
        return Advise.objects.filter(usser=self.request.user).values('adviser__username', 'advise', 'recompdate', 'rstocks__stockName', 'reason')

    










#commented code in portfoliodetailview after context object name-----------------------------------------
# def get_labels_and_data(self):
    #     labels = []
    #     data = []
    #     # pname = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('portfolioName', flat=True)
    #     pname = UserPortfolioStock.objects.filter(portfolio=self.kwargs['pk']).values_list('stockName', flat=True)
    #     pscore = UserPortfolioStock.objects.filter(portfolio=self.kwargs['pk']).values_list('currentPrice', flat=True)

    #     # pname = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('portfolioName',flat=True).get()
    #     # pname =Portfolio.objects.filter().values_list('portfolioName',flat=True)
    #     # pscore = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('portfolioScore', flat=True)

    #     for i in pname:
    #         labels.append(i)
    #     for i in pscore:
    #         data.append(i)

    #     return labels, data








# class UserPortfolioStockListView(ListView):
#     model = UserPortfolioStock
#     template_name = 'stocks/portfoliodetails.html'
#     context_object_name = 'ups'
    
#     def get_queryset(self):
#         # Get the portfolio name from the URL parameter
#         portfolio_name = self.request.GET.get('portfolioName', '')
        
#         # Filter the UserPortfolioStock queryset based on the portfolio name
#         queryset = UserPortfolioStock.objects.filter(portfolio__portfolioName=portfolio_name)
        
#         return queryset


 # if userporfolio.exclude(stocks__isnull=True).exists():  
        #   if userporfolio.doesnotexists():
        #   message = "No user portfolio stock found matching the query."
        #   print(message)
    
        # # Handle the case where no results are returned
        #     message = "No user portfolio stock found matching the query."
        #     # partial = render_to_string('stocks/partial_template.html', {'message': message})
        #     return render(request, self.template_name, {'portfoliodetails': self.get_object(), 'portfolio': portfolio, 'message': message})
        # userporfolio = UserPortfolioStock.objects.filter(portfolio=self.kwargs['pk']).select_related('stock').values()

#Not in use portfoliodetail view ------------------------------------------------------------
# @method_decorator([login_required(login_url='/user/login'),euser_required],name='dispatch')
# class PortfolioDetailView(DetailView):
#     model = UserPortfolioStock
#     template_name = 'stocks/portfoliodetails.html'
#     context_object_name = 'portfoliodetails'

    
#     labels=[]
#     data=[]

#     pname = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('id',flat=True)
#     pscore = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('portfolioScore',flat=True)
        
#     for i in pname:
#             labels.append(i)
#     for i in pscore:
#             data.append(i)
    

     
    # def get(self, request, *args, **kwargs):
    #     # print(f"self.kwargs['pk'] = {self.kwargs['pk']}")
    #     print(f"request.user = {request.user}")
    #     portfolio = Portfolio.objects.filter(userportfoliostock=self.kwargs['pk'],user=request.user).values()
    #     # print(f"portfolio = {portfolio}")
    #     userporfolio = UserPortfolioStock.objects.filter(portfolio=self.kwargs['pk'])
    #     portfolioName = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('portfolioName',flat=True).get()
    #     pid = Portfolio.objects.filter(id=self.kwargs['pk']).values_list('id',flat=True).get()
        

        
        
        
    
        
        

    #     print(userporfolio)
    #     if request.method == 'GET':
    #            price_sort = request.GET.get('price_sort')
    #     if price_sort == 'asc':
    #            userporfolio = userporfolio.order_by('currentPrice')
    #     elif price_sort == 'desc':
    #            userporfolio = userporfolio.order_by('-currentPrice')  
       
              
        
    #     return render(request, self.template_name, {'portfoliodetails': self.get_object(),'portfolio':portfolio,'ups':userporfolio,'portfolioName':portfolioName,'pid':pid,'labels':self.labels,'data':self.data})
        
    # def get_object(self, queryset=None):
    #     try:
    #         return super().get_object(queryset)
    #     except Http404:
    #         return redirect('portfoliodetail', pk=self.kwargs['pk'])


#commented code for stock list view------------------------------------------------------------
#     queryset = super().get_queryset()
    #     queryset = queryset.filter(user=self.request.user)
    #     return queryset

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     price_filter = self.request.GET.get('price_filter')
    #     if price_filter:
    #         min_price, max_price = price_filter.split('-')
    #         queryset = queryset.filter(currentPrice__gte=min_price, currentPrice__lte=max_price)
    #     return queryset
        

# def calculate_total_difference(portfolio_id):
#     total_difference = 0
#     for stock in UserPortfolioStock.objects.filter(portfolio=portfolio_id):
#         difference = stock.currentPrice - stock.investPrice
#         total_difference += difference
    
#     return total_difference
#     print(f"total_difference = {total_difference}")