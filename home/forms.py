from django import forms 
from home.models import *
  
class ShipForm(forms.ModelForm): 
  
    class Meta: 
        model = ShipDetection 
        # fields = ['ship_img', 'satellite_scale']
        fields = ['ship_img']
