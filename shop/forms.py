from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "email", "address", "city", "postal_code")
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }
