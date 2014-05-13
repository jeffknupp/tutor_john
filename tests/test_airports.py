"""Test for airports."""

import json
from airports import load_airport_info, AIRPORT_CODES, AIRPORT_LOCATIONS, app, get_zoom

def test_airports_are_loaded():
    """Can we successfully load airport info from a file?"""
    load_airport_info('us_airports.txt')
    assert len(AIRPORT_CODES) == 2843
    assert 'LGA' in AIRPORT_CODES
    assert 'LGA' in AIRPORT_LOCATIONS
    assert len(AIRPORT_LOCATIONS) == 1362

def test_default_route():
    """Can we successfully load the form page?"""
    client = app.test_client()
    app.testing = True
    response = client.get('/')
    assert 'Airport Distance' in response.get_data()

def test_completions():
    """Do completions for a given term get returned correctly?"""
    client = app.test_client()
    app.testing = True
    response = client.get('/completions?term=lax')
    assert json.loads(response.get_data()) == [{"value": "LAX", "label": "Los Angeles Intl (LAX)"}]

def test_resulting_map():
    """Does the resulting map display correctly?"""
    client = app.test_client()
    app.testing = True
    response = client.post('/get_distance.html', data={'origin': 'EWR', 'destination': 'LAX'})
    as_text = response.get_data()
    assert 'LatLng(39.4442535904, -97.3351527597)' in as_text
    assert 'LatLng (33.942536, -118.408075)' in as_text
    assert '(40.6925, -74.168667)' in as_text

def test_get_zoom():
    """Do we return the appropriate zoom level based on distances?"""
    assert get_zoom(3000) == 4
    assert get_zoom(1300) == 5
    assert get_zoom(600) == 6
    assert get_zoom(50) == 9
