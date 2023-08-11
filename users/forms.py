from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from products.models import ShippingInfo


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = "__all__"
        exclude = ["order"]
