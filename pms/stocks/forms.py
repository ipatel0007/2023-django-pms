from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Stocks

class EuserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name','last_name','email', 'password1','password2','phone_no','address','annual_income')
        
    Widgets = {

        'username': forms. TextInput (attrs= {'class': 'form-control', 'placeholder': 'username'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        'last_name': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        'email': forms.EmailInput (attrs={'class': 'form-control', 'placeholder': 'Email'}), 
        'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}), 
        'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter Password'}),
        'phone_no': forms.NumberInput(attrs= {'class': 'form-control', 'placeholder': 'phonenumber'}),
        'address': forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'address'}),
        'annual_income': forms.NumberInput(attrs= {'class': 'form-control', 'placeholder': 'annual income'}),



    }

class StocksCreationForm(forms.ModelForm):
    class Meta:
        model = Stocks
        fields = '__all__'
        
    # Widgets = {
    #     'name': forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'name'}),
    #     'price': forms.NumberInput(attrs= {'class': 'form-control', 'placeholder': 'price'}),
    #     'sector': forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'sector'}),
    #     'quantity': forms.NumberInput(attrs= {'class': 'form-control', 'placeholder': 'quantity'}),
    #     'date': forms.DateInput(attrs= {'class': 'form-control', 'placeholder': 'date'}),
    # }

  


        
