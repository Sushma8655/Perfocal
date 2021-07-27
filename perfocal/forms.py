from django.forms import ModelForm, DateTimeInput,DateInput
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AddMachine(forms.ModelForm):
    class Meta:
        model = AddMachine
        fields = ['MachineID','MachineName','AssetID','Capacity']