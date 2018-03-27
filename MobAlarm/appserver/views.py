# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from appserver.models import User, Location


from appserver.datamanager import downloadDataFromGoogle, category_list
from appserver.gridmanager import computeGridId, computeNearbyGridId, getLocationsInGrids, computeInnterBox, range_dict, computeNearbyGridIdwithDirection, handle_location

import bz2
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as U
from django.contrib.auth.decorators import login_required

import requests





def user_register(request, username, password):
    # response with fail message if username exist
    try:
        user = U.objects.get(username=username)
        encrypted_password = None
    except U.DoesNotExist:
        user = None
        encrypted_password = bz2.compress(password.encode('utf-8'))

    if user is not None:
        status = dict(type='post_response', status='fail', reason='username has already been used')
        return JsonResponse(status, safe=False)

    # register auth user
    new_u = U(username=username, password=encrypted_password)
    new_u.save()

    # add new user to User table
    new_user = User(username=new_u.username)
    new_user.save()

    status = dict(type='post_response', status='succeed', reason='register succeeded')
    return JsonResponse(status, safe=False)


def user_login(request, username, password):
    user, u = verifyUser(username)
    # print(u)

    input_password = str(bz2.compress(password.encode('utf-8')))
    # print(input_password)


    test = authenticate(username='ll')
    print(test)

    # reponse with fail message if username does not exist
    if u is None:
        status = dict(type='post_response', status='fail', reason='user does not exist')
        return JsonResponse(status, safe=False)

    # check password
    if u is not None and input_password != u.password:
        # print("wrong password")
        status = dict(type='post_response', status='fail', reason='wrong password')
        return JsonResponse(status, safe=False)

    # login
    login(request, u)
    status = dict(type='post_response', status='succeed', reason='user login succeeded')
    return JsonResponse(status, safe=False)


def add_event(request, username, category):
    user, u = verifyUser(username)

    # if not request.user.is_authenticated:
    #     print("here")

    # reponse with fail message if username does not exist
    if user is None:
        status = dict(type='post_response', status='fail', reason='user does not exist')
        return JsonResponse(status, safe=False)

    # reponse with fail message if category is not supported
    if category not in category_list:
        status = dict(type='post_response', status='fail', reason='wrong category')
        return JsonResponse(status, safe=False)
    # register user with the category
    user.__dict__[category] = True
    user.save()
    status = dict(type='post_response', status='succeed', reason='event is added successfully')
    return JsonResponse(status, safe=False)


def delete_event(request, username, category):
    user, u = verifyUser(username)

    # reponse with fail message if username does not exist
    if user is None:
        status = dict(type='post_response', status='fail', reason='user does not exist')
        return JsonResponse(status, safe=False)
    # reponse with fail message if categories does not exist
    if category not in category_list:
        status = dict(type='post_response', status='fail', reason='wrong category')
        return JsonResponse(status, safe=False)
    # unregister user with the category
    user.__dict__[category] = False
    user.save()
    status = dict(type='post_response', status='succeed', reason='event is deleted successfully')

    # status = dict(type = 'post_response', status = 'succeed', reason = 'event is deleted successfully')
    return JsonResponse(status, safe=False)



def handle_location_with_angle(request, username, latitude, longitude, angle):
    user, u = verifyUser(username)
    status = handle_location(user, latitude, longitude, angle)

    return JsonResponse(status, safe=False)

def handle_location_without_angle(request, username, latitude, longitude):
    user, u = verifyUser(username)
    status = handle_location(user, latitude, longitude, angle = -1)
    return JsonResponse(status, safe=False)


# admin method for grabbing location data from GOOGLE API, and put locationw with grid_id into online database
# !!!!!!!!!!!!DO NOT run this function, or database may get in trouble!!!!!!!!!!!
def process_data(request, password, category):
    status = downloadDataFromGoogle(password, category)
    return JsonResponse(status, safe=False)






# the function is for user authentication
def verifyUser(username):
    try:
        user = User.objects.get(username=username)
        u = U.objects.get(username=username)
    except User.DoesNotExist:
        user = None
        u = None
    return user, u
