# Generated by Django 4.2.3 on 2023-08-01 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0003_biometrics_heartbeatvar_biometrics_respiratoryrate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biometrics',
            name='heartBeat',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='biometrics',
            name='heartBeatVar',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='biometrics',
            name='respiratoryRate',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='biometrics',
            name='restingHeartRate',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
