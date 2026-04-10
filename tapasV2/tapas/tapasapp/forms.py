from django import forms
from .models import Account

class SignupForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password']
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 150)
    password = forms.CharField(widget = forms.PasswordInput)