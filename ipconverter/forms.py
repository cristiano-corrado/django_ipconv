from django import forms
from .models import IPChaos


class IPForm(forms.ModelForm):
    class Meta:
        model = IPChaos

        fields = ['string',"type"]


class InputForm(forms.Form):
    ipinsert = forms.CharField(label='Copy and Paste your list of ip/cidr/netmasks',widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = IPChaos
        fields = {'string','type'}
