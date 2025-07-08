from django import forms

class AFPForm(forms.Form):
    rut = forms.CharField(
        required=True,
        label='RUT de la AFP',
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        required=True,
        label='Nombre de la AFP',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )