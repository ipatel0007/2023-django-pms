from django.shortcuts import render
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.views.generic import ListView,DetailView
from .forms import *

from .models import Stocks

# Create your views here.
# def getAllStocks(request):
    
#     #select * from products
#     stocks = Stocks.objects.all().values()
#     #products = Product.objects.all().values_list('pName','pPrice','pQty')
#     #products = Product.objects.all().values('pName','pPrice','pQty')
#     #fetch single object
#     #product =Product.objects.get(id=1)
#     #price greater thn....
#     #__ django orm lookups
#     #products  = Product.objects.filter(pPrice__gte = 800).values()
#     #products  = Product.objects.filter(pPrice__lte = 800).values()
#     #products = Product.objects.filter(pName__startswith='i').values()
#     #products = Product.objects.filter(pName__icontains='P').values()
#     #orderby
#     #products = Product.objects.all().order_by('-pName').values()
#     print(stocks)
#     return render(request,'allstocks.html',{'stocks':stocks})


class StocksListView(ListView):
    model = Stocks
    template_name = 'stocks/liststocks.html'
    context_object_name = 'stockslist'

class StocksCreateView(CreateView):
    fields = '__all__'
    model = Stocks
    template_name = 'stocks/createstock.html'
    success_url = '/user/euserdash'

class StockDeleteView(DeleteView):
    model = Stocks
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/user/euserdash/'   



class StockUpdateView(UpdateView):
    model = Stocks
    form_class = StocksCreationForm
    template_name = 'stocks/createstock.html'
    success_url = '/user/euserdash/'

    
