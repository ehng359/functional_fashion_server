# Generated by Django 4.2.3 on 2023-07-25 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='biometrics',
            name='date',
            field=models.CharField(default='', max_length=18),
        ),
    ]
