from django import forms

from .models import NewVehicle,rule_engine
from django.forms import ModelForm

class NewVehicleForm(ModelForm):                    #importing models from models
    class Meta:
        model = NewVehicle
        fields = '__all__'
        widgets = {                         #used this to add placeholder
            'Service_Count':forms.NumberInput(attrs={'placeholder':'0 for New Vehicle'}),
            'Previous_Service_Odo':forms.NumberInput(attrs={'placeholder':'0 for new Vehicle'}),
            'Previous_Service_Date':forms.DateInput(attrs={'placeholder':'0 for New Vehicle'}),
            'Register_No': forms.TextInput(attrs={'placeholder':'ex:KA01MN9999'})
        }


class rule_engineForm(ModelForm):               #rule engine form
    class Meta:
        model = rule_engine
        fields = '__all__'



#for service details update
class Update_serviceForm(forms.Form):
    Register_No = forms.CharField(max_length=20)            #to take reg_No
    current_odo = forms.FloatField()                        #for enter the odo
    Service_completion_date = forms.DateField(label="Service Completion Date(YYYY-MM-DD) ")

#for the odo meter update
class Update_odo_readingForm(forms.Form):
    Register_No = forms.CharField(max_length=20)
    current_odo = forms.FloatField()
