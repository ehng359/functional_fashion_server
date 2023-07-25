# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Biometrics(models.Model):
    date = models.CharField(max_length=19, default="")
    heartBeat = models.IntegerField()