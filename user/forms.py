from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['nickname', 'email', 'username', 'password1', 'password2']
        
        
# class LoginUpForm(forms.ModelForm):
    
#     class Meta:
#         model = CustomUser
#         fiel