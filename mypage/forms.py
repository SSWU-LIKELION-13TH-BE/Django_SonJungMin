from django import forms
from django.contrib.auth.forms import UserChangeForm
from user.models import CustomUser


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['nickname', 'email', 'username']
        widgets = {
            'password': forms.HiddenInput(),
        }