from django import forms


class ImportBooksForm(forms.Form):
    json_file = forms.FileField(label='Select JSON File')
