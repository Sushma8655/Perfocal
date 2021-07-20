# Generated by Django 3.2 on 2021-07-12 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='initiateMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elementID', models.CharField(max_length=300)),
                ('installationMaintenanceDate', models.DateTimeField(null=True)),
                ('nextDueDate', models.DateTimeField(null=True)),
                ('initiateStatus', models.CharField(max_length=300)),
                ('initiateTimestamp', models.DateTimeField(null=True)),
                ('ackStatus', models.CharField(max_length=300)),
                ('ackTimestamp', models.DateTimeField(null=True)),
                ('closeStatus', models.CharField(max_length=300)),
                ('closeTimestamp', models.DateTimeField(null=True)),
                ('repairUpdateCycle', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='maintenanceAcknowledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elementAID', models.CharField(max_length=300)),
                ('initialisedDate', models.DateTimeField()),
                ('nextDueDate', models.DateField()),
                ('status', models.CharField(max_length=300)),
                ('acknowledgeTimeStamp', models.DateField(auto_now=True)),
                ('initID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ackIDs', to='maintenance.initiatemaintenance')),
            ],
        ),
        migrations.CreateModel(
            name='partRegistry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('partsID', models.CharField(max_length=300, unique=True)),
                ('servicePeriod', models.IntegerField()),
                ('servicePeriodDMY', models.CharField(max_length=300)),
                ('conditionBased', models.CharField(max_length=300)),
                ('usageBased', models.CharField(max_length=300, null=True)),
                ('maintainRequired', models.CharField(max_length=300, null=True)),
                ('upperLimit', models.CharField(max_length=300, null=True)),
                ('dueThreshold', models.CharField(max_length=300, null=True)),
                ('overDueThreshold', models.CharField(max_length=300, null=True)),
                ('dueValueCycle', models.CharField(max_length=300, null=True)),
                ('overDueCycle', models.CharField(max_length=300, null=True)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='maintenanceClose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elementCID', models.CharField(max_length=300)),
                ('initialisedDate', models.DateTimeField()),
                ('nextDueDate', models.DateField()),
                ('status', models.CharField(max_length=300)),
                ('closeTimeStamp', models.DateTimeField()),
                ('ackID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maintenance.maintenanceacknowledge')),
            ],
        ),
    ]
