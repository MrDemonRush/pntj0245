from django import forms

class UploadJSONForm(forms.Form):
    file =forms.FileField()
