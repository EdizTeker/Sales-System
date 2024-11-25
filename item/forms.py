from django import forms
from .models import Item, Cart
from django.forms import modelformset_factory

class ItemForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = [
            'cartnumber',
        ]
        labels = {
            'cartnumber': 'Quantity',
        }

     