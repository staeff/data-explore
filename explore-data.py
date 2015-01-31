#!/usr/bin/env python
# coding=utf-8

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

Steps:

* check whether 'output/' and 'sourcedata/' exist. if not create them
* check if data file exists in 'output/' if not download

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

# currently not used
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

# currently not used
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


def visualize_values(counter, name):
    """Visualize data by category in a bar graph"""

    # Set the labels which are based on the keys of our counter.
    # labels needed to be utf-8 decoded, otherwise plt.xticks
    # broke with unicode-decode-error
    # tuple instead of list for performance?
    labels = tuple([i.decode('utf-8') for i in counter.keys()])

    fullpath_outfile = "output/{0}.png".format(name)

    # Set where the labels hit the x-axis
    xlocations = np.arange(len(labels)) + 0.5

    # Width of each bar
    width = 0.5

    # Assign data to a bar plot
    plt.bar(xlocations, counter.values(), width=width)

    #import ipdb; ipdb.set_trace()

    # Assign labels and tick location to x- and y-axis
    plt.xticks(xlocations + width / 2, labels, rotation=90)
    plt.yticks(range(0, max(counter.values()), 5))

    # Give some more room so the labels aren't cut off in the graph
    plt.subplots_adjust(bottom=0.4)

    # Make the overall graph/figure larger
    plt.rcParams['figure.figsize'] = 12, 8

    # Save the graph!
    plt.savefig(fullpath_outfile)

    # Close figure
    plt.clf()


def main():
    arg_parser = argparse.ArgumentParser()
    # example call:
    # > python accidents.py --csvfile file.csv
    arg_parser.add_argument('--csvfile', '-f',
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
    # dataobject as variable name sucks, because its totally nondescriptive
    dataobject = {}
    keys = data[0].keys()

    for i in keys:
        lower_case_category_name = i.lower()
        dataobject[lower_case_category_name] = create_counters(i, data)
        visualize_values(dataobject[lower_case_category_name], lower_case_category_name)

    return dataobject

if __name__ == "__main__":
    dataobject = main()
    print(dataobject.keys())
