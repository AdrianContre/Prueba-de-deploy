from django import forms
from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'banner', 'first_name','last_name', 'bio']

class MyForm(forms.Form):
    ORDER_CHOICES = [
        ('Nou', 'New'),
        ('Antic', 'Old'),
        ('Més comentaris', 'Most comments'),
        ('El millor de tots els temps', 'The best(El NANO)'),
    ]
    order = forms.ChoiceField(choices=ORDER_CHOICES, widget=forms.Select(attrs={'class': 'dropdown-item'}))


class CercaForm(forms.Form):
    Form_CHOICES = [
        ('Publicacions', 'cercapub'),
        ('Comentaris', 'cercacom'),
    ]
    order = forms.ChoiceField(choices=Form_CHOICES, widget=forms.Select(attrs={'class': 'dropdown-item'}))


class TextForm(forms.Form):
    text_input = forms.CharField(max_length=100)


class TextComForm(forms.Form):
    text_input = forms.CharField(max_length=500)
