"""Web application that calculates the distance between two airports."""
import math
import sys
import json

from flask import Flask, render_template, request

EARTHS_RADIUS_IN_NAUTICAL_MILES = 3440.07

AIRPORT_LOCATIONS = {}
AIRPORT_CODES = {}

app = Flask(__name__)

def load_airport_info(airport_file):
    """Load latitude, longitude, airport code, and airport name from file."""
    with open(airport_file, 'r') as file_handle:
        for line in file_handle:
            line = line.split(',')
            name, code, latitude, longitude = line[1].strip('"'), line[4].strip('"'), float(line[6]), float(line[7])
            AIRPORT_LOCATIONS[code] = (latitude, longitude)
            AIRPORT_CODES[code] = '{name} ({code})'.format(name=name, code=code)
            AIRPORT_CODES[name.upper()] = '{name} ({code})'.format(name=name, code=code)

@app.route('/completions', methods=['GET'])
def get_completions():
    """Return possible completions for a given request parameter."""
    term = request.args['term'].upper()
    completions = []
    
    for key in AIRPORT_CODES:
        if key.startswith(term):
            completions.append({'label': AIRPORT_CODES[key], 'value': key})
    return json.dumps(completions)

@app.route('/', methods=['GET'])
def display_form():
    return render_template('index.html')

@app.route('/get_distance.html', methods=['POST'])
def display_results():
    """Show results on map."""
    origin_name = request.form['origin']
    destination_name = request.form['destination']
    origin = AIRPORT_LOCATIONS[origin_name]
    destination = AIRPORT_LOCATIONS[destination_name]
    midpoint = get_midpoint(origin, destination)
    distance = get_distance_in_nautical_miles(origin, destination)
    return render_template('get_distance.html', midpoint=midpoint,
            destination_location=destination, origin_location=origin,
            distance=distance, zoom=get_zoom(distance))

def main():
    """Main entry point for program."""
    load_airport_info('us_airports.txt')
    app.run(debug=True)
    pass

def get_zoom(distance):
    """Back of the envelope calculation for appropriate 
    Google Maps zoom level"""
    if distance > 2000:
        return 4
    elif distance > 1000:
        return 5
    elif distance > 500:
        return 6
    else:
        return 9


def get_distance_in_nautical_miles(origin, destination):
    """Return distance between two locations in nautical miles.

    `origin` and `destination` are expected to be a tuple comprised of
    latitude, longitude where both are expressed in decimal form.

    Again, formula shamelessly stolen from Internet.
    """

    (lat1, lon1) = [math.radians(x) for x in origin]
    (lat2, lon2) = [math.radians(x) for x in destination]

    return int(math.acos(
        math.sin(lat1) * math.sin(lat2) +
        math.cos(lat1) * math.cos(lat2) *
        math.cos(lon2 - lon1)) *
        EARTHS_RADIUS_IN_NAUTICAL_MILES)


def get_midpoint(origin, destination):
    """Returns the midpoint latitude and longitude between the points given
    
    Formula shamelessly stolen from Internet
    """
    (lat1, lon1) = [math.radians(x) for x in origin]
    (lat2, lon2) = [math.radians(x) for x in destination]

    dlon = lon2 - lon1
    dx = math.cos(lat2) * math.cos(dlon)
    dy = math.cos(lat2) * math.sin(dlon)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), math.sqrt((math.cos(lat1) + dx) * (math.cos(lat1) + dx) + dy * dy))
    lon3 = lon1 + math.atan2(dy, math.cos(lat1) + dx)

    return(math.degrees(lat3), math.degrees(lon3))


if __name__ == '__main__':
    sys.exit(main())
