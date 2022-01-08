from . import models
from django import forms
from django.forms.fields import DateField

class DateInput(forms.DateInput):
    input_type = 'date'

class AttendenceForm(forms.ModelForm):
    class Meta:
        model = models.attendence_schedule
        fields = ('date',)
        widgets = {'date':DateInput(),}
