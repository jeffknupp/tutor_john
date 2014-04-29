"""Web application that calculates the distance between two airports."""

import sys
from flask import Flask, render_template, request
import json

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
    return str(request.form)

def main():
    """Main entry point for program."""
    load_airport_info('us_airports.txt')
    app.run(debug=True)
    pass

if __name__ == '__main__':
    sys.exit(main())
