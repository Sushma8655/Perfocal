from django.db import models

# Create your models here.
class partRegistry(models.Model):
    name =models.CharField(max_length=300)
    partsID = models.CharField(max_length=300, unique=True)
    servicePeriod = models.IntegerField()
    servicePeriodDMY = models.CharField(max_length=300)
    conditionBased = models.CharField(max_length=300)
    usageBased = models.CharField(max_length=300, null=True)
    maintainRequired = models.CharField(max_length=300 , null=True)
    upperLimit = models.CharField(max_length=300, null=True)
    dueThreshold = models.CharField(max_length=300, null=True)
    overDueThreshold = models.CharField(max_length=300, null=True)
    dueValueCycle = models.CharField(max_length=300, null=True)
    overDueCycle = models.CharField(max_length=300, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.partsID)


class initiateMaintenance(models.Model):
    elementID = models.CharField(max_length=300)
    installationMaintenanceDate = models.DateTimeField(null=True)
    nextDueDate = models.DateTimeField(null=True)
    initiateStatus = models.CharField(max_length=300)
    initiateTimestamp = models.DateTimeField(null=True)
    ackStatus = models.CharField(max_length=300)
    ackTimestamp = models.DateTimeField(null=True)
    closeStatus = models.CharField(max_length=300)
    closeTimestamp = models.DateTimeField(null=True)
    repairUpdateCycle = models.CharField(max_length=300, null=True)


class maintenanceAcknowledge(models.Model):
    initID = models.ForeignKey(initiateMaintenance, related_name='ackIDs', on_delete=models.CASCADE)
    elementAID = models.CharField(max_length=300)
    initialisedDate = models.DateTimeField()
    nextDueDate = models.DateField()
    status = models.CharField(max_length=300)
    acknowledgeTimeStamp = models.DateField(auto_now=True)

class maintenanceClose(models.Model):
    ackID = models.ForeignKey(maintenanceAcknowledge, on_delete=models.CASCADE)
    elementCID = models.CharField(max_length=300)
    initialisedDate = models.DateTimeField()
    nextDueDate = models.DateField()
    status = models.CharField(max_length=300)
    closeTimeStamp = models.DateTimeField()

