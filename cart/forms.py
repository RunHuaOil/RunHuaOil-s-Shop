from django import forms
from django.utils.translation import gettext_lazy as _


class CartAddProductForm(forms.Form):
        
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    quantity = forms.IntegerField(label=_('购买数量'), initial=1)

    # def clean_quantity(self):
    #     cd = self.cleaned_data
    #     self.data.get('stock', '100')
    #     if cd['quantity'] == '':
    #         raise forms.ValidationError('不能为空')
    #     return cd['quantity']
