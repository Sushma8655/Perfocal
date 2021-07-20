from django.forms import DateTimeInput, DateInput
from django import forms
from .models import *

DMYChoices = [
    ('', 'Make Choice'),
    ('Days', 'Days'),
    ('Weeks', 'Weeks'),
    ('Months', 'Months'),

]
conditionBased = [
    ('', 'Make Choice'),
    ('Applicable', 'Applicable'),
    ('NA', 'NA'),
]
usageBased =[
    ('', 'Make Choice'),
    ('Direct Measurement', 'Direct Measurement'),
    ('Continuous Cycle', 'Continuous Cycle'),
    ('NA', 'NA'),
]
maintainRequired = [
    ('', 'Make Choice'),
    ('Value Exceeds the Limit', 'Value Exceeds the Limit'),
    ('Value Falls Below the Limit', 'Value Falls Below the Limit'),
    ('Value Deviates from certain range', 'Value Deviates from certain range'),
    ('NA', 'NA'),
]
repairUpdateCycle = [
    ('', 'Make Choice'),
    ('Yes','Yes'),
    ('No','No'),

]
class registryForm(forms.ModelForm):
    servicePeriodDMY = forms.CharField(label='', widget=forms.Select(choices=DMYChoices))
    conditionBased = forms.CharField(label='Condition Based', widget=forms.Select(choices=conditionBased, attrs={'onchange':'ddSelect()'}))
    usageBased = forms.CharField(label='Usage Based', widget=forms.Select(choices=usageBased, attrs={'onchange':'ddSelect()'}))
    maintainRequired = forms.CharField(label='Maintenance Required if', widget=forms.Select(choices=maintainRequired) )
    class Meta:
        model = partRegistry
        fields = ['name', 'partsID', 'servicePeriod', 'servicePeriodDMY', 'conditionBased', 'usageBased',
                  'maintainRequired', 'upperLimit', 'dueThreshold', 'overDueThreshold', 'dueValueCycle',
                  'overDueCycle']


class maintenanceInitiate(forms.ModelForm):
    elementID = forms.ModelChoiceField(queryset=partRegistry.objects.all(), to_field_name='partsID', required=False)
    # status = forms.CharField(label='status', widget=forms.TextInput(attrs={'value':'Initiated','type':'hidden'}))
    class Meta:
        model = initiateMaintenance
        fields = ['elementID', 'installationMaintenanceDate']
        widgets ={
            'installationMaintenanceDate':DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'nextDueDate':DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }
        exclude = ['user']


class maintenanceAcknowledge(forms.ModelForm):
    elementID = forms.ModelChoiceField(queryset=initiateMaintenance.objects.values_list('elementID', flat=True).filter(initiateStatus="Initiated"),
                                       to_field_name='elementID',required=False)
    class Meta:
        model = initiateMaintenance
        fields = ['elementID']

class maintenanceClose(forms.ModelForm):
    elementID = forms.ModelChoiceField(
        queryset=initiateMaintenance.objects.values_list('elementID', flat=True).filter(ackStatus="Acknowledged"),
        to_field_name='elementID', required=False)
    repairID = forms.ModelChoiceField(queryset=initiateMaintenance.objects.values_list('elementID', flat=True).filter(initiateStatus="Repair"),
        to_field_name='elementID', required=False)
    class Meta:
        model = initiateMaintenance
        fields = ['elementID', 'closeTimestamp', 'repairID']
        widgets ={
            'closeTimestamp': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }
        exclude = ['user']

class reparirForm(forms.ModelForm):
    elementID = forms.ModelChoiceField(queryset=partRegistry.objects.all(), to_field_name='partsID', required=False)
    repairUpdateCycle = forms.CharField(label='', widget=forms.Select(choices=repairUpdateCycle))
    # status = forms.CharField(label='status', widget=forms.TextInput(attrs={'value':'Initiated','type':'hidden'}))
    class Meta:
        model = initiateMaintenance
        fields = ['elementID', 'installationMaintenanceDate', 'repairUpdateCycle']
        widgets = {
            'installationMaintenanceDate': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            # 'nextDueDate': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }


# class maintenanceAck(forms.ModelForm):
#     elementAID = forms.ModelChoiceField(queryset=initiateMaintenance.objects.values_list('elementID',flat=True), to_field_name='elementID', required=False)
#     class Meta:
#         model = maintenanceAcknowledge
#         fields = ['elementAID']
#
# class maintenanceClose(forms.ModelForm):
#     elementCID = forms.ModelChoiceField(queryset=maintenanceAcknowledge.objects.values_list('elementAID',flat=True), to_field_name='elementAID', required=False)
#     class Meta:
#         model = maintenanceClose
#         fields = ['elementCID', 'closeTimeStamp']
#         widgets = {
#             'closeTimeStamp': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
#         }
#         exclude = ['user']
