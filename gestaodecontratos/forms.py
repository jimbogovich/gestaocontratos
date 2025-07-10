from msilib.schema import CheckBox
from tkinter.tix import Select
from .models import contactManagement_db, STATUS, Reminder, Client
from django.contrib.auth.models import User
import re
from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True)
    class Meta:
        model=User
        fields = ("username", "email", "password1", "password2")

class ContratosForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=STATUS,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = contactManagement_db
        fields = '__all__'


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = '__all__'
        widgets = {
            'reminder_date': forms.DateInput(attrs={'type': 'date'}),
            'recipients': forms.SelectMultiple(attrs={'size': '4'}),
        }
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'cnpjoucpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_cnpjoucpf(self):
        value = self.cleaned_data['cnpjoucpf']
        digits = re.sub(r'\D', '', value)

        def is_valid_cpf(cpf):
            if len(cpf) != 11 or cpf == cpf[0] * 11:
                return False
            for i in range(9, 11):
                total = 0
                for j in range(0, i):
                    total += int(cpf[j]) * ((i + 1) - j)
                digit = ((total * 10) % 11) % 10
                if int(cpf[i]) != digit:
                    return False
            return True

        def is_valid_cnpj(cnpj):
            if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
                return False
            weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            weights2 = [6] + weights1
            for weights, i in ((weights1, 12), (weights2, 13)):
                total = sum(int(d) * w for d, w in zip(cnpj[:i], weights))
                digit = (total % 11)
                digit = 0 if digit < 2 else 11 - digit
                if int(cnpj[i]) != digit:
                    return False
            return True

        if len(digits) == 11 and is_valid_cpf(digits):
            return value
        elif len(digits) == 14 and is_valid_cnpj(digits):
            return value
        else:
            raise forms.ValidationError("Informe um CPF ou CNPJ válido.")




