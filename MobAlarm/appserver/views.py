# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from appserver.models import User, Location

import requests

#alternative google api keys: AIzaSyDlkmBMSsJUym5t-HlCj3SsBiHr3TWdPhI

google_place_api = 'AIzaSyBuDt53ewEt-mkV8AV5tJrjnd5-Se1DoEk'
place_search_api_prefix = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location=33.775622,-84.398473&radius=5000&type='
place_detail_api_prefix = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='

#atlanta boundary
range_dict = dict(top = 33.875448, bottom = 33.575448, left = -84.563182, right = -84.263182)

#divide atlanta into an 66 * 66 grid system
num_of_col = 66
num_of_row = 66

#current support categories
category_list= ['supermarket', 'gasstation', 'postoffice', 'atm', 'shoppingmall']


#neighbor grids in grid system
dx = [1, 0, -1]
dy = [1, 0, -1]


def user_register(request, username):

        #response with fail message if username exist
        try:
                user = User.objects.get(username = username)
        except User.DoesNotExist:
                user = None

        if user is not None:
                status = dict(type = 'post_response', status = 'fail', reason = 'username has already been used')
                return JsonResponse(status, safe = False)

        #register username
        new_user = User(username = username)
        new_user.save()

        status = dict(type = 'post_response', status = 'succeed', reason = 'register succeeded')
        return JsonResponse(status, safe =False)

def user_login(request, username):

        user = verifyUser(username)
        #reponse with fail message if username does not exist
        if user is None:
                status = dict(type = 'post_response', status = 'fail', reason = 'user does not exist')
                return JsonResponse(status, safe = False)

        status = dict(type = 'post_response', status = 'succeed', reason = 'user login succeeded') 
        return JsonResponse(status, safe =False)


def add_event(request, username, category):
        user = verifyUser(username)
        #reponse with fail message if username does not exist
        if user is None:
                status = dict(type = 'post_response', status = 'fail', reason = 'user does not exist')
                return JsonResponse(status, safe = False)

        #reponse with fail message if category is not supported
        if category not in category_list:
                status = dict(type = 'post_response', status = 'fail', reason = 'wrong category')
                return JsonResponse(status, safe = False)
        #register user with the category
        user.__dict__[category] = True
        user.save()
        status = dict(type = 'post_response', status = 'succeed', reason = 'event is added successfully')
        return JsonResponse(status, safe =False)
	

def delete_event(request, username, category):
        user = verifyUser(username)
        #reponse with fail message if username does not exist
        if user is None:
                status = dict(type = 'post_response', status = 'fail', reason = 'user does not exist')
                return JsonResponse(status, safe = False)
        #reponse with fail message if categories does not exist
        if category not in category_list:
                status = dict(type = 'post_response', status = 'fail', reason = 'wrong category')
                return JsonResponse(status, safe = False)
        #unregister user with the category
        user.__dict__[category] = False
        user.save()
	status = dict(type = 'post_response', status = 'succeed', reason = 'event is deleted successfully')
        return JsonResponse(status, safe =False)


def handle_location(request, username, latitude, longitude):
        user = verifyUser(username)
       
        #reponse with fail message if username does not exist
        if user is None:
                status = dict(type = 'post_response', status = 'fail', reason = 'user does not exist')
                return JsonResponse(status, safe = False)

        lng = float(longitude)
        lat = float(latitude)

        #reponse with fail message if user is not in supporte area
        if lng < range_dict['left'] or lng > range_dict['right'] or lat < range_dict['bottom'] or lat > range_dict['top']:
                status = dict(type = 'post_response', status = 'fail', reason = 'user out of range')
                return JsonResponse(status, safe = False)

        #update user's current grid_id
        user.last_grid_id = computeGridId(latitude, longitude)
        user.save()

        userEvents = []

        #get all register event of the user
        for category in category_list:
                if user.__dict__[category] is True:
                        userEvents.append(category)

        #compute nearby grids
        nearbyGridIds = computeNearbyGridId(latitude, longitude)

        #compute locations in nearby grids
        nearbyLocations = getLocationsInGrids(nearbyGridIds, userEvents)
        
        #compute the request-free inner box for the user, and a set of notifiable results
        innerbox, results= computeInnterBox(nearbyLocations, user.last_grid_id, lat, lng)

        # reponse with results and the innerbox
        status = dict(type = 'result_set', box = innerbox, numberOfResult = len(results), results = results)
        return JsonResponse(status , safe =False)

#admin method for grabbing location data from GOOGLE API, and put locationw with grid_id into online database 
#!!!!!!!!!!!!DO NOT run this function, or database may get in trouble!!!!!!!!!!!
def process_data(request, password,category):
	if password == 'meow':
                url = place_search_api_prefix + category + '&key=' + google_place_api
                r = requests.get(url)
                results = r.json()['results']
        else:
                res_status = dict(status = 'fail', numOfResult = len(results))
                return JsonResponse(res_status, safe =False)

        for item in results:

        	place_id = item['place_id']
        	lat = item['geometry']['location']['lat']
        	lng = item['geometry']['location']['lng']

                if lng < range_dict['left'] or lng > range_dict['right'] or lat < range_dict['bottom'] or lat > range_dict['top']:
                        continue

        	detail_url = place_detail_api_prefix + place_id + '&key=' + google_place_api
        	detail_r = requests.get(detail_url)
        	detail_result = detail_r.json()['result']

        	business_address = detail_result['formatted_address']
        	business_name = detail_result['name']
        	business_grid_id = computeGridId(lat, lng)
        	#business_description = ???
          
        	new_business = Location(category = category, name = business_name, grid_id = business_grid_id , latitude = lat, longitude = lng, address = business_address)
        	new_business.save()


        res_status = dict(status = 'success', numOfResult = len(results))
        return JsonResponse(res_status, safe =False)

#given coordinates, compute the grid_id
def computeGridId(lat, lng):
	#the gird has 44 rows and 66 cols
	row = int((range_dict['top'] - float(lat))*110000)//500
	col = int((float(lng) - range_dict['left'])*110000)//500  
        print(row, col)
	return row*num_of_col + col


#given a grid_id, given all the neighbors' gird_id
def computeNearbyGridId(lat, lng):
        grid_id = computeGridId(lat, lng)

        row_id = grid_id//num_of_col
        col_id = grid_id%num_of_col

        result = []

        for i in dx:
                for j in dy:
                        x = row_id + i
                        y = col_id + j

                        if x >=0 and y >=0 and x < num_of_row and y < num_of_col:
                                result.append(x * num_of_col + y)
        
        return result
                      
#return satisfying locations
def getLocationsInGrids(nearbyGridIds, userEvents):
        print(nearbyGridIds)
        print(userEvents)
        locations = Location.objects.filter(grid_id__in = nearbyGridIds).filter(category__in = userEvents)
        
        return locations

#compute the innerbox
def computeInnterBox(nearbyLocations, grid_id, user_lat, user_lng):
        row_id = grid_id//num_of_col
        col_id = grid_id%num_of_col

        #the 3*3 gird neighborhood servers as a default box
        top = min(range_dict['top'] - ((row_id - 1) * 0.0045), range_dict['top'])
        bottom  = max(range_dict['top'] - ((row_id + 2) * 0.0045), range_dict['bottom'])
        left = max(range_dict['left'] + ((col_id - 1) * 0.0045), range_dict['left'])
        right = min(range_dict['left'] + ((col_id + 2) * 0.0045), range_dict['right'])

        results = []

        #the innerbox shrinks as testing each candidate locations in the 3*3 neighborhood
        for location in nearbyLocations:
                l = float(location.longitude) - 0.0005
                r = float(location.longitude) + 0.0005
                t = float(location.latitude) + 0.0005
                b = float(location.latitude) - 0.0005
                print(l, r, t, b, location.longitude, location.latitude)

                #Locations in user's range will not be considered for computing the innerbox, they will be added to the result lists.
                if user_lat < t and user_lat > b and user_lng < r and user_lng > l:
                        item = dict(name = location.name, category = location.category, latitude = location.latitude ,longitude = location.longitude, description = "Blank")
                        results.append(item)
                        continue

                if l > user_lng and l < right:
                        right = l

                if r < user_lng and r > left:
                        left = r

                if b > user_lat and b < top:
                        top = b

                if t < user_lat and t > bottom:
                        bottom = t

        return dict(top = top, bottom = bottom, left = left, right = right), results
      


# the function is for user authentication
def verifyUser(username):
        try:
                user = User.objects.get(username = username)
        except User.DoesNotExist:
                user = None
        return user
	





