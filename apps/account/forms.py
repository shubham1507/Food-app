from django import forms
from django.contrib.auth import password_validation, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from apps.account.models import User, City


class RegisterForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    city = forms.ChoiceField(choices=City.objects.values_list("name", "name"), label="City")
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    class Meta:
        model = User
        fields = ["email"]


class LoginForm(forms.Form):
    user = None
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            self.add_error("password", "Wrong credentials!")
        return cleaned_data
