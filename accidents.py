#!/usr/bin/env python

"""
Explorative data analysis of DB_ACC_2014.csv - DESCRIPTION of the Data here.

Fields in Data:
DILIG,
LUGAR - Ort,
ALTURA_DE - Hoehe von (Strassenkreuzung),
FECHA - Datum,
HORA - Stunde,
VEHICULOS - Fahrzeuge,
HERIDOS - Wunden,
DESTINO - Ziel,
COLISION - Kollision (Zusammenstoss),
INFR_COND - ?,
INFR_PEAT - ?,
DENUNCIAS - Anzeigen

Questions/Ideas

* interpolate or extrapolate position with Lugar and Altura
* transform date fecha into weekdays, years, months
* determine oldest and youngest entry to show what time is covered
* load file from web, so it does not have to be in the repo and I don't have
to worry about licenses.
* group time value by hours and/or daytime
* sanity check data (I already have seen some spelling errors.) There are
probably different spellings of the same street.




"""

from collections import Counter # http://pymotw.com/2/collections/counter.html

import argparse # http://pymotw.com/2/argparse/index.html#module-argparse
import csv      # http://pymotw.com/2/csv/index.html#module-csv
import geojson
import matplotlib.pyplot as plt
import numpy as np


def load_data(raw_file, delimiter):
    """Parses a raw CSV file to a JSON-like object"""

    # Ich koennte versuchen, ob das Ding mit with immer noch
    # das gleiche macht
    opened_file = open(raw_file)

    # Read the CSV data
    csv_data = csv.reader(opened_file, delimiter=delimiter)

    # Setup an empty list
    parsed_data = []

    # Skip over the first line of the file for the headers
    fields = csv_data.next()
    strip_fields = [i.strip() for i in fields]

    # Iterate over each row of the csv file, zip together field -> value
    for row in csv_data:
        parsed_data.append(dict(zip(strip_fields, row)))

    # Close the CSV file
    opened_file.close()

    return parsed_data

def create_counters(key, datafile):
    """ creates counter objects of every column of data-file.
        With that we have the frequency data of

        About counter objects see:
        http://pymotw.com/2/collections/counter.html
    """
    counter = Counter(item[key] for item in datafile)
    return counter

def get_dates(datafile):
    """ Do something with the dates
        Figuring out which weekday a certain day was is another step.
        with that information, its possible to do the same analysis as
        the original, i.e. show accidents by weekday

        * accidents per month
        * accidents per year
        * accidents per weekday
     """

    # counter can be accessed like a dictionary
    # ie. counter["05/12/2014"]
    dates = Counter(item["FECHA"] for item in data)
    return dates

def get_places(datafile):
    """ Which is the place with the most accidents.

    """

    # counter can be accessed like a dictionary
    places = Counter(item["LUGAR"] for item in data)
    return places

def visualize_days(data_file):
    """Visualize data by day of week"""

    # Returns a dict where it sums the total values for each key.
    # In this case, the keys are the DaysOfWeek, and the values are
    # a count of incidents.
    counter = Counter(item["DayOfWeek"] for item in data_file)

    # Separate out the counter to order it correctly when plotting.
    data_list = [counter["Monday"],
                 counter["Tuesday"],
                 counter["Wednesday"],
                 counter["Thursday"],
                 counter["Friday"],
                 counter["Saturday"],
                 counter["Sunday"]
                 ]

    # Why?
    day_tuple = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])
    # Why not day_tuple = tuple("Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun")

    # Assign the data to a plot
    plt.plot(data_list)

    # Assign labels to the plot
    plt.xticks(range(len(day_tuple)), day_tuple)

    # Save the graph!
    plt.savefig("Days.png")

    # Close figure
    plt.clf()


def visualize_type(data_file):
    """Visualize data by category in a bar graph"""

    # That looks easy - I should try that out in the shell
    counter = Counter(item["Category"] for item in data_file)

    # Set the labels which are based on the keys of our counter.
    labels = tuple(counter.keys())

    # Set where the labels hit the x-axis
    xlocations = np.arange(len(labels)) + 0.5

    # Width of each bar
    width = 0.5

    # Assign data to a bar plot
    plt.bar(xlocations, counter.values(), width=width)

    # Assign labels and tick location to x- and y-axis
    plt.xticks(xlocations + width / 2, labels, rotation=90)
    plt.yticks(range(0, max(counter.values()), 5))

    # Give some more room so the labels aren't cut off in the graph
    plt.subplots_adjust(bottom=0.4)

    # Make the overall graph/figure larger
    plt.rcParams['figure.figsize'] = 12, 8

    # Save the graph!
    plt.savefig("Type.png")

    # Close figure
    plt.clf()


def create_map(data_file):
    """Creates a GeoJSON file.

    Returns a GeoJSON file that can be rendered in a GitHub
    Gist at gist.github.com.  Just copy the output file and
    paste into a new Gist, then create either a public or
    private gist.  GitHub will automatically render the GeoJSON
    file as a map.
    """

    # Define type of GeoJSON we're creating
    geo_map = {"type": "FeatureCollection"}

    # Define empty list to collect each point to graph
    item_list = []

    # Iterate over our data to create GeoJSOn document.
    # We're using enumerate() so we get the line, as well
    # the index, which is the line number.
    for index, line in enumerate(data_file):

        # Skip any zero coordinates as this will throw off
        # our map.
        if line['X'] == "0" or line['Y'] == "0":
            continue

        # Setup a new dictionary for each iteration.
        data = {}

        # Assigne line items to appropriate GeoJSON fields.
        data['type'] = 'Feature'
        data['id'] = index
        data['properties'] = {'title': line['Category'],
                              'description': line['Descript'],
                              'date': line['Date']}
        data['geometry'] = {'type': 'Point',
                            'coordinates': (line['X'], line['Y'])}

        # Add data dictionary to our item_list
        item_list.append(data)

    # For each point in our item_list, we add the point to our
    # dictionary.  setdefault creates a key called 'features' that
    # has a value type of an empty list.  With each iteration, we
    # are appending our point to that list.
    for point in item_list:
        geo_map.setdefault('features', []).append(point)

    # Now that all data is parsed in GeoJSON write to a file so we
    # can upload it to gist.github.com
    with open('file_sf.geojson', 'w') as f:
        f.write(geojson.dumps(geo_map))


def main():
    arg_parser = argparse.ArgumentParser()
    # example call:
    # > python accidents.py --csvfile file.csv
    arg_parser.add_argument('--csvfile',
                            help="Parses the given CSV/Excel file. The full\
                            path to the file is needed.",
                            type=str, required=True)
    arg_parser.add_argument('--delimiter',
                            help="Delimiter of the Input File",
                            type=str, default=",")
    # Returns a dictionary of keys = argument flag, and value = argument
    args = vars(arg_parser.parse_args())

    # Parse data
    data = load_data(args['csvfile'], args['delimiter'])

    # how do i dynamically create variable names? Maybe this is solved, because
    # i am not assigning to variables, but create dataobject.
    dataobject = {}
    for i in data[0].keys():
        dataobject[i.lower()] = create_counters(i, data)

    return dataobject

if __name__ == "__main__":
    dataobject = main()
    print(dataobject.keys())
