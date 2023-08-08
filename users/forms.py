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

    # def __init__(self, *args, **kwargs):
    #     super(ProfileSettingsForm, self).__init__(*args, **kwargs)
    #     # Add customizations to form fields here, if needed
    #     self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
    #     self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
    #     self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
    #     # self.fields['profile_picture'].widget.attrs['placeholder'] = 'Enter a URL for your profile picture'
    #     # self.fields['bio'].widget.attrs['placeholder'] = 'Enter a short bio'
    #
    #     # You can also add custom CSS classes to form fields like this:
    #     self.fields['first_name'].widget.attrs['class'] = 'form-control'
    #     self.fields['last_name'].widget.attrs['class'] = 'form-control'
    #     self.fields['email'].widget.attrs['class'] = 'form-control'
    #     # self.fields['profile_picture'].widget.attrs['class'] = 'form-control'
    #     # self.fields['bio'].widget.attrs['class'] = 'form-control'


class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = "__all__"
        exclude = ["order"]
