# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User, Location
# Register your models here.

class LocationAdmin(admin.ModelAdmin):
	list_display = ['category', 'name', 'latitude', 'longitude', 'grid_id', 'address']

class UserAdmin(admin.ModelAdmin):
	list_display = ['username','last_grid_id']

admin.site.register(Location, LocationAdmin)
admin.site.register(User, UserAdmin)