from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from apps.models import User, Newsletter_emails


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-type Password'}))

    def clean_username(self):
        username = self.data.get('username')
        if User.objects.filter(username=username):
            raise ValidationError("This username already exist !")
        return username

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email):
            raise ValidationError("This email already exist !")
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Confirm password is incorrect!')
        return make_password(password)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def check_user(self):
        username = self.data.get('username')
        password = self.data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise ValidationError("Invalid username or password !")
        return self.cleaned_data


class EmailForm(forms.ModelForm):
    def clean_email(self):
        email = self.data.get('email')
        if Newsletter_emails.objects.filter(email=email):
            raise ValidationError("This email already exists !")
        return email

    class Meta:
        model = Newsletter_emails
        fields = ('email',)
