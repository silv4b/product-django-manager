from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input w-full', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'input w-full h-32 py-2', 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'class': 'input w-full', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': 'input w-full', 'placeholder': '0'}),
        }
