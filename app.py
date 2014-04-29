"""Web application that calculates the distance between two airports."""

import sys

AIRPORT_LOCATIONS = {}
AIRPORT_CODES = {}

def load_airport_info(airport_file):
    """Load latitude, longitude, airport code, and airport name from file."""
    with open(airport_file, 'r') as file_handle:
        for line in file_handle:
            line = line.split(',')
            name, code, latitude, longitude = line[1].strip('"'), line[4].strip('"'), float(line[6]), float(line[7])
            AIRPORT_LOCATIONS[code] = (latitude, longitude)
            AIRPORT_CODES[code] = '{name} ({code})'.format(name=name, code=code)
            AIRPORT_CODES[name] = '{name} ({code})'.format(name=name, code=code)

def get_completions():
    """Return possible autocompletions for a given snippet of text."""
    pass

def display_form():
    """Display airport form."""
    pass

def display_results():
    """Show results on map."""
    pass

def main():
    """Main entry point for program."""
    pass

if __name__ == '__main__':
    load_airport_info('us_airports.txt')
    print AIRPORT_CODES['EWR']
    print AIRPORT_LOCATIONS['EWR']
    print AIRPORT_CODES['Newark Liberty Intl']
    sys.exit(main())
