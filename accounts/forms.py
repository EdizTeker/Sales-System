from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username', widget=forms.TextInput)
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)

    

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Wrong value')
        return super(LoginForm, self).clean()

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='Username')
    email = forms.CharField(label='email', widget=forms.EmailInput, required=True)
    password1 = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label='Password again', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']    

    def clean_password2(self):
        password1 =self.cleaned_data.get('password1')
        password2 =self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The passwords do not match.")
        return password2