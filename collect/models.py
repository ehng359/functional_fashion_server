# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=40, default="")
    biometricData = models.ManyToManyField('Biometrics', blank=True, null=True)

    def __str__(self):
        return self.id

# Create your models here.
class Biometrics(models.Model):
    watchUser = models.ForeignKey(Users,blank=True, null=True, on_delete=models.DO_NOTHING)
    date = models.CharField(max_length=30, default="")

    # Biometric label values
    heartBeat = models.IntegerField(default=None, null=True)
    respiratoryRate = models.IntegerField(default=None, null=True)
    heartBeatVar = models.IntegerField(default=None, null=True)
    restingHeartRate = models.IntegerField(default=None, null=True)

    # Emotion-Spectrum Grid Values
    valence = models.FloatField(default=None, null=True)
    arousal = models.FloatField(default=None, null=True)

    # Context
    activity = models.CharField(max_length=20, default="None")

    def __str__(self):
        return self.watchUser.id + " " + self.date
