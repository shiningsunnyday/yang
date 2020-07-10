from django import forms

class YangForm(forms.Form):
    input = forms.CharField(label='Type your favorite former presidential candidate', max_length=100)