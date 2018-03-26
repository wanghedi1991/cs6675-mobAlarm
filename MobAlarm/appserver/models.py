# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as U
from django.conf import settings

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length = 100)
	# username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	# password = models.TextField(null = True)
	last_grid_id = models.IntegerField(default = -1)
	supermarket = models.BooleanField(default = False)
	gasstation = models.BooleanField(default = False)
	atm = models.BooleanField(default = False)
	postoffice = models.BooleanField(default = False)
	shoppingmall = models.BooleanField(default = False)



class Location(models.Model):
	category = models.CharField(max_length = 100)
	name = models.CharField(max_length = 200)
	grid_id = models.IntegerField(db_index = True)
	latitude = models.DecimalField(decimal_places = 6, max_digits = 8)
	longitude = models.DecimalField(decimal_places = 6, max_digits = 8)
	address = models.TextField(null = True)
	description = models.TextField(null = True, blank = True)
    