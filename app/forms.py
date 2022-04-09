from app.models import Customer
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms import fields
from django.forms import widgets
from django.forms.widgets import PasswordInput, Widget
from django.utils.translation import gettext, gettext_lazy as _


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='conferm password (again)',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', required=True,  widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        lebels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={'autofocus': True, 'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label=_("password"), strip=False,  widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("old password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'autofocun': True, 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_("new password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("confirm new password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254,  widget=forms.EmailInput(
        attrs={'autocomplete': 'email', 'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("new password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("confirm new password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'zipcode', 'state']
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'locality': forms.TextInput(attrs={'class': 'form-control'}),
        'city': forms.TextInput(attrs={'class': 'form-control'}),
        'state': forms.TextInput(attrs={'class': 'form-control'}),
        'zipcode': forms.TextInput(attrs={'class': 'form-control'})
        }