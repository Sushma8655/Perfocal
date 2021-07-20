from django.db import models

# Create your models here.

class AddMachine(models.Model):
    MachineID = models.IntegerField(primary_key=True)
    MachineName = models.CharField(max_length=255)
    Capacity = models.IntegerField()
    logo = models.ImageField()
    AssetID = models.CharField(max_length=100, null=False, blank=False,)

    def __str__(self):
        return str(self.MachineID)