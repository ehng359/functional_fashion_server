# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Biometrics
from .models import Users
# Register your models here.
admin.site.register(Biometrics)
admin.site.register(Users)
