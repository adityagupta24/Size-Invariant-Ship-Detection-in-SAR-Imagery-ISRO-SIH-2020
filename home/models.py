from django.db import models

# Create your models here.

class ShipDetection(models.Model):
    ship_img = models.ImageField(blank = False, upload_to='images/') 
    # scale = models.FloatField(blank = False, name = 'satellite_scale')