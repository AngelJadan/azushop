from django import forms
from django.contrib.auth.models import User

from ventas.models import Product

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','username','first_name', 'last_name', 'password')


class FormProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "key","name","price","description","iva","image"
        ]
        labels = {
            "key":"Key",
            "name":"Name",
            "price":"Price",
            "description":"Description",
            "iva":"IVA",
            "image":"Image"
        }
        widgets = {
            "key":forms.TextInput(attrs={"class":"form-control form-label", "title":"Key",}),
            "name":forms.TextInput(attrs={"class":"form-control form-label", "title":"Name",}),
            "price":forms.NumberInput(attrs={"min":"0","class":"form-control form-label", "title":"price", "style":"width:50px;"}),
            "description":forms.Textarea(attrs={"class":"form-control form-label","rows":"2", "cols":"20"}),
            "iva":forms.Select(choices=Product.IVA),
            'image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'},),
        }
