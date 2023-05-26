from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import EnrollmentRequest, User
from stocks.models import *

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

  

class AdvisorRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1','password2')

        Widgets = {

        'username': forms. TextInput (attrs= {'class': 'form-control', 'placeholder': 'username'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        'last_name': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        'email': forms.EmailInput (attrs={'class': 'form-control', 'placeholder': 'Email'}), 
        'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}), 
        'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter Password'}),
       



    }
        
class EnrollmentRequestForm(forms.ModelForm):
    class Meta:
        model = EnrollmentRequest
        fields = ['user', 'advisor', 'status']
        widgets = {
            'user': forms.HiddenInput(),
            'advisor': forms.HiddenInput(),
            'status': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['status'] = 'PENDING'
    

    
class StockAdviseForm(forms.ModelForm):
    
    usser = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    adviser = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    advise = forms.ChoiceField(choices=Advise.advise_choices, widget=forms.Select(attrs={'class': 'form-control','placeholder':'Advise'}) )
    recompdate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date'}))
    rstocks = forms.ModelChoiceField(queryset=Stocks.objects.all(), empty_label="Select Stock", widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Stocks'}))
    reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'reason'}))
    class Meta:
        model = Advise
        fields = '__all__'

    


class EnrollmentRequestUpdateForm(forms.ModelForm):
    
    # status = forms.ModelChoiceField(queryset=EnrollmentRequest.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=EnrollmentRequest.status_choices, widget=forms.Select(attrs={'class': 'form-control'}) )
    
    class Meta:
        model = EnrollmentRequest
        fields = ['status']

      
        





# class EnrollmentRequestUpdateForm(forms.ModelForm):
#     STATUS_CHOICES = (
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     )

#     status = forms.ChoiceField(choices=STATUS_CHOICES)

#     class Meta:
#         model = EnrollmentRequest
#         fields = ('status',)

# class EnrollmentRequestUpdateForm(forms.ModelForm):
#     class Meta:
#         model = EnrollmentRequest
#         fields = ['status']
#         widgets = {
#             'status': forms.Select(choices=[('approve', 'Approve'), ('reject', 'Reject')])
#         }