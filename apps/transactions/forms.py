from django import forms
from .models import Transaction

class TransferForm(forms.Form):
    destination_card = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border rounded-lg',
            'placeholder': 'شماره کارت مقصد',
            'pattern': '[0-9]{16}',
            'title': 'شماره کارت باید 16 رقم باشد'
        }),
        label='شماره کارت مقصد'
    )
    
    amount = forms.IntegerField(
        min_value=10000,
        max_value=50000000,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 border rounded-lg',
            'placeholder': 'مبلغ به ریال'
        }),
        label='مبلغ (ریال)'
    )
    
    def clean_destination_card(self):
        card = self.cleaned_data['destination_card']
        if not card.isdigit():
            raise forms.ValidationError('شماره کارت باید فقط شامل اعداد باشد')
        return card