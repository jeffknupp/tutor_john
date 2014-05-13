import json
from airports import load_airport_info, AIRPORT_CODES, AIRPORT_LOCATIONS, app

def test_airports_are_loaded():
    load_airport_info('us_airports.txt')
    assert len(AIRPORT_CODES) == 2843
    assert 'LGA' in AIRPORT_CODES
    assert 'LGA' in AIRPORT_LOCATIONS
    assert len(AIRPORT_LOCATIONS) == 1362

def test_default_route():
    client = app.test_client()
    app.testing = True
    response = client.get('/')
    assert 'Airport Distance' in response.get_data()

def test_completions():
    client = app.test_client()
    app.testing = True
    response = client.get('/completions?term=lax')
    assert json.loads(response.get_data()) == [{"value": "LAX", "label": "Los Angeles Intl (LAX)"}]
