from typing import Any

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordMixin
from django.core import validators

from accounts.models import User


class SignUpForm(forms.ModelForm, SetPasswordMixin):
    class Meta:
        model = User
        fields = ['email']

    password1, password2 = SetPasswordMixin.create_password_fields()
    password1.required = True
    password2.required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email já cadastrado.')
        return email

    def clean(self):
        self.validate_passwords()
        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user = self.set_password_and_save(user, commit=commit)
        return user


class SignInForm(forms.Form):
    email = forms.CharField(validators=[validators.EmailValidator()])
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self) -> dict[str, Any]:
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        self.user = authenticate(username=email, password=password)
        if not self.user:
            self.add_error(None, 'Credenciais inválidas.')

        return super().clean()
