from __future__ import unicode_literals

from django.db import models
from appserver.models import User, Location
from appserver.gridmanager import computeGridId, computeNearbyGridId, getLocationsInGrids, computeInnterBox, range_dict, computeNearbyGridIdwithDirection, handle_location


google_place_api = 'AIzaSyBuDt53ewEt-mkV8AV5tJrjnd5-Se1DoEk'
place_search_api_prefix = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location=33.775622,-84.398473&radius=5000&type='
place_detail_api_prefix = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='

category_list = ['supermarket', 'gasstation', 'postoffice', 'atm', 'shoppingmall']


def downloadDataFromGoogle(password, category):
    if password == 'meow':
        url = place_search_api_prefix + category + '&key=' + google_place_api
        r = requests.get(url)
        results = r.json()['results']

    else:
        res_status = dict(status='fail')
        return res_status

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
    return res_status