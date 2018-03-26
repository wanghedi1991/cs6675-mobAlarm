from __future__ import unicode_literals

from django.db import models
from appserver.models import User, Location
category_list = ['supermarket', 'gasstation', 'postoffice', 'atm', 'shoppingmall']

# neighbor grids in grid system
dx = [1, 0, -1]
dy = [1, 0, -1]

num_of_col = 66
num_of_row = 66
# atlanta boundary
range_dict = dict(top=33.875448, bottom=33.575448, left=-84.563182, right=-84.263182)

# given coordinates, compute the grid_id
def computeGridId(lat, lng):
    # the gird has 44 rows and 66 cols
    row = int((range_dict['top'] - float(lat)) * 110000) // 500
    col = int((float(lng) - range_dict['left']) * 110000) // 500
    print(row, col)

    return row * num_of_col + col



#input a clockwise angle from the north, in the range[0, 360)
def computeNearbyGridIdwithDirection(lat, lng, angle):
    grid_id = computeGridId(lat, lng)

    row_id = grid_id // num_of_col
    col_id = grid_id % num_of_col
    result = []

    if (angle >= 0 and angle < 45) or (angle >= 315 and angle < 360) :
        for i in range(-1, 2):
            for j in (-1, 1):
                x = row_id + i
                y = col_id + j

                if x >= 0 and y >= 0 and x < num_of_row and y < num_of_col:
                    result.append(x * num_of_col + y)

    elif angle >= 45 and angle < 135:
        for i in range(0, 2):
            for j in (-1, 2):
                x = row_id + i
                y = col_id + j

                if x >= 0 and y >= 0 and x < num_of_row and y < num_of_col:
                    result.append(x * num_of_col + y)

    elif angle >= 135 and angle < 225:
        for i in range(-1, 2):
            for j in (0, 2):
                x = row_id + i
                y = col_id + j

                if x >= 0 and y >= 0 and x < num_of_row and y < num_of_col:
                    result.append(x * num_of_col + y)

    elif angle >=225 and angle < 315:
        for i in range(-1, 1):
            for j in (-1, 2):
                x = row_id + i
                y = col_id + j

                if x >= 0 and y >= 0 and x < num_of_row and y < num_of_col:
                    result.append(x * num_of_col + y)
    return result


# given a grid_id, given all the neighbors' gird_id
def computeNearbyGridId(lat, lng):
    grid_id = computeGridId(lat, lng)

    row_id = grid_id // num_of_col
    col_id = grid_id % num_of_col

    result = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            x = row_id + i
            y = col_id + j

            if x >= 0 and y >= 0 and x < num_of_row and y < num_of_col:
                result.append(x * num_of_col + y)

    return result


# return satisfying locations
def getLocationsInGrids(nearbyGridIds, userEvents):
    print(nearbyGridIds)
    print(userEvents)

    locations = Location.objects.filter(grid_id__in=nearbyGridIds).filter(category__in=userEvents)

    return locations


# compute the innerbox
def computeInnterBox(nearbyLocations, grid_id, user_lat, user_lng):
    row_id = grid_id // num_of_col
    col_id = grid_id % num_of_col

    # the 3*3 gird neighborhood servers as a default box
    top = min(range_dict['top'] - ((row_id - 1) * 0.0045), range_dict['top'])
    bottom = max(range_dict['top'] - ((row_id + 2) * 0.0045), range_dict['bottom'])
    left = max(range_dict['left'] + ((col_id - 1) * 0.0045), range_dict['left'])
    right = min(range_dict['left'] + ((col_id + 2) * 0.0045), range_dict['right'])

    results = []

    # the innerbox shrinks as testing each candidate locations in the 3*3 neighborhood
    for location in nearbyLocations:
        l = float(location.longitude) - 0.0005
        r = float(location.longitude) + 0.0005
        t = float(location.latitude) + 0.0005
        b = float(location.latitude) - 0.0005
        print(l, r, t, b, location.longitude, location.latitude)

        # Locations in user's range will not be considered for computing the innerbox, they will be added to the result lists.
        if user_lat < t and user_lat > b and user_lng < r and user_lng > l:
            item = dict(name=location.name, category=location.category, latitude=location.latitude,
                        longitude=location.longitude, description="Blank")
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

    return dict(top=top, bottom=bottom, left=left, right=right), results

def handle_location(user, latitude, longitude, angle = -1):
     # reponse with fail message if username does not exist
    if user is None:
        status = dict(type='post_response', status='fail', reason='user does not exist')
        return status

    lng = float(longitude)
    lat = float(latitude)

    # reponse with fail message if user is not in supporte area
    if lng < range_dict['left'] or lng > range_dict['right'] or lat < range_dict['bottom'] or lat > range_dict['top']:
        status = dict(type='post_response', status='fail', reason='user out of range')
        return status

    # update user's current grid_id
    user.last_grid_id = computeGridId(latitude, longitude)
    user.save()

    userEvents = []

    # get all register event of the user
    for category in category_list:
        if user.__dict__[category] is True:
            userEvents.append(category)

    # compute nearby grids
    if angle == -1:
        nearbyGridIds = computeNearbyGridId(latitude, longitude)
    else:
        nearbyGridIds = computeNearbyGridIdwithDirection(latitude, longitude, angle)
   
    # compute locations in nearby grids
    nearbyLocations = getLocationsInGrids(nearbyGridIds, userEvents)

    # compute the request-free inner box for the user, and a set of notifiable results
    innerbox, results = computeInnterBox(nearbyLocations, user.last_grid_id, lat, lng)

    # reponse with results and the innerbox
    status = dict(type='result_set', box=innerbox, numberOfResult=len(results), results=results)
    return status



