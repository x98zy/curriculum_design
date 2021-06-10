from django import forms

class DeviceForm(forms.Form):
    device_name=forms.CharField(max_length=50,required=True)
    imsi=forms.CharField(max_length=50,required=True)