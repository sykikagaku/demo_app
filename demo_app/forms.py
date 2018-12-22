from django import forms # Djangoが準備しているforms
from .models import Customers # モデルの部分で定義したDBのテーブル

from django.forms.widgets import NumberInput


class RangeInput(NumberInput):
    input_type = 'range'
    input_oninput = "document.getElementById('output').value=this.value"

class InputForm(forms.ModelForm):
    limit_balance = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=200000)
    bill_amt_1 = forms.IntegerField(widget=RangeInput(), min_value=-200000, max_value=100000)
    pay_amt_1 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_2 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_3 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_4 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_5 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_6 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)


    class Meta:
        model = Customers
        exclude = ['id', 'result', 'proba', 'comment', 'registered_date']
        widgets = {
        'last_name' : forms.TextInput(attrs={'placeholder':'last_name'}),
        'first_name' : forms.TextInput(attrs={'placeholder':'first_name'}),
        }
