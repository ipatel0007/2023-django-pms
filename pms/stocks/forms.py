from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Stocks,UserPortfolioStock,Portfolio



class StocksCreationForm(forms.ModelForm):
        stocks = forms.ModelChoiceField(queryset=Stocks.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
        
        portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
          
        class Meta:
         model = UserPortfolioStock
         fields = ('stocks','portfolio','qty','purchaseDate','investPrice','currentPrice',)

        
        # fields = '__all__'
        
        Widgets = {

        
        # 'user': forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'user'}),
        # 'portfolio': forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'portfolio'}),
        'qty': forms.NumberInput(attrs= {'class': 'form-control', 'placeholder': 'quantity'}),
        'purchaseDate': forms.DateInput(attrs= {'class': 'form-control', 'placeholder': 'date'}),
        'investPrice': forms.NumberInput(attrs= {'class': 'form-control', 'placeholder': 'invest price'}),
        'currentPrice': forms.NumberInput(attrs= {'class': 'form-control', 'placeholder': 'current price'}),
        
    }   
        
        
         
       

       


class StocksUpdateForm(forms.ModelForm):
    
    
    
    stocks = forms.ModelChoiceField(queryset=Stocks.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'quantity'}))
    purchaseDate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'date'}))
    investPrice = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'invest price'}))
    currentPrice = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'current price'}))
    
    class Meta:
        model = UserPortfolioStock
        fields = ('stocks', 'qty', 'purchaseDate', 'investPrice', 'currentPrice',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['qty'].initial = instance.qty
            self.fields['purchaseDate'].initial = instance.purchaseDate
            self.fields['investPrice'].initial = instance.investPrice
            self.fields['currentPrice'].initial = instance.currentPrice



class PortfolioCreateForm(forms.ModelForm):
    
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Portfolio
        fields = ('user','portfolioName',)
    
    Widgets = {
     
     
    'portfolioName' : forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'portfolio name'}))



    }

  


        
