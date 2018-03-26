# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from appserver.models import User, Location
from gridmanager import computeGridId, computeNearbyGridId, getLocationsInGrids, computeInnterBox, range_dict
import bz2
import base64

import requests

# alternative google api keys: AIzaSyDlkmBMSsJUym5t-HlCj3SsBiHr3TWdPhI

google_place_api = 'AIzaSyBuDt53ewEt-mkV8AV5tJrjnd5-Se1DoEk'
place_search_api_prefix = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location=33.775622,-84.398473&radius=5000&type='
place_detail_api_prefix = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='




# current support categories
category_list = ['supermarket', 'gasstation', 'postoffice', 'atm', 'shoppingmall']


def user_register(request, username, password):
    # response with fail message if username exist
    try:
        user = User.objects.get(username=username)
        encrypted_password = None
    except User.DoesNotExist:
        user = None
        encrypted_password = bz2.compress(password.encode('utf-8'))

    if user is not None:
        status = dict(type='post_response', status='fail', reason='username has already been used')
        return JsonResponse(status, safe=False)

    # register username
    new_user = User(username=username, password=encrypted_password)
    new_user.save()

    status = dict(type='post_response', status='succeed', reason='register succeeded')
    return JsonResponse(status, safe=False)


def user_login(request, username, password):
    user = verifyUser(username)

    input_password = str(bz2.compress(password.encode('utf-8')))
    # print(input_password)

    # reponse with fail message if username does not exist
    if user is None:
        status = dict(type='post_response', status='fail', reason='user does not exist')
        return JsonResponse(status, safe=False)

    # check password
    if user is not None and input_password != user.password:
        # print("wrong password")
        status = dict(type='post_response', status='fail', reason='wrong password')
        return JsonResponse(status, safe=False)

    status = dict(type='post_response', status='succeed', reason='user login succeeded')
    return JsonResponse(status, safe=False)


def add_event(request, username, category):
    user = verifyUser(username)
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
    user = verifyUser(username)
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


def handle_location(request, username, latitude, longitude):
    user = verifyUser(username)

    # reponse with fail message if username does not exist
    if user is None:
        status = dict(type='post_response', status='fail', reason='user does not exist')
        return JsonResponse(status, safe=False)

    lng = float(longitude)
    lat = float(latitude)

    # reponse with fail message if user is not in supporte area
    if lng < range_dict['left'] or lng > range_dict['right'] or lat < range_dict['bottom'] or lat > range_dict['top']:
        status = dict(type='post_response', status='fail', reason='user out of range')
        return JsonResponse(status, safe=False)

    # update user's current grid_id
    user.last_grid_id = computeGridId(latitude, longitude)
    user.save()

    userEvents = []

    # get all register event of the user
    for category in category_list:
        if user.__dict__[category] is True:
            userEvents.append(category)

    # compute nearby grids
    nearbyGridIds = computeNearbyGridId(latitude, longitude)

    # compute locations in nearby grids
    nearbyLocations = getLocationsInGrids(nearbyGridIds, userEvents)

    # compute the request-free inner box for the user, and a set of notifiable results
    innerbox, results = computeInnterBox(nearbyLocations, user.last_grid_id, lat, lng)

    # reponse with results and the innerbox
    status = dict(type='result_set', box=innerbox, numberOfResult=len(results), results=results)
    return JsonResponse(status, safe=False)


# admin method for grabbing location data from GOOGLE API, and put locationw with grid_id into online database
# !!!!!!!!!!!!DO NOT run this function, or database may get in trouble!!!!!!!!!!!
def process_data(request, password, category):
    if password == 'meow':
        url = place_search_api_prefix + category + '&key=' + google_place_api
        r = requests.get(url)
        results = r.json()['results']

    else:

        res_status = dict(status='fail')
        return JsonResponse(res_status, safe=False)

    for item in results:

        place_id = item['place_id']
        lat = item['geometry']['location']['lat']
        lng = item['geometry']['location']['lng']

        if lng < range_dict['left'] or lng > range_dict['right'] or lat < range_dict['bottom'] or lat > range_dict[
            'top']:
            continue

        detail_url = place_detail_api_prefix + place_id + '&key=' + google_place_api
        detail_r = requests.get(detail_url)
        detail_result = detail_r.json()['result']

        business_address = detail_result['formatted_address']
        business_name = detail_result['name']
        business_grid_id = computeGridId(lat, lng)
        # business_description = ???

        new_business = Location(category=category, name=business_name, grid_id=business_grid_id, latitude=lat, longitude=lng,
                            address=business_address)
        new_business.save()

    res_status = dict(status='success', numOfResult=len(results))
    return JsonResponse(res_status, safe=False)






# the function is for user authentication
def verifyUser(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user
