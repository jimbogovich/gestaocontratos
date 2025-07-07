from msilib.schema import CheckBox
from tkinter.tix import Select

from .models import contactManagement_db, STATUS, Reminder
from django import forms
import datetime


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


