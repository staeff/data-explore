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

* create subfolders in 'output' for results of different data sets
* create requirements.txt for easy install of new packages. (create new
virtual environment and see whats not working)

Questions/Ideas

* sanity check data (I already have seen some spelling errors.) There are
probably different spellings of the same street.

### explore the data

* look at the diagrams for easy analysises

### processing of location

* Try to turn street names into location data. Use an API? Is there one?

### processing of Dates

* transform date fecha into weekdays, years, months - date parsing with python
* determine oldest and youngest entry to show what time is covered
* group time value by hours and/or daytime

"""

from collections import Counter # http://pymotw.com/2/collections/counter.html

import argparse # http://pymotw.com/2/argparse/index.html#module-argparse
import csv      # http://pymotw.com/2/csv/index.html#module-csv
import os
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

def visualize_values(counter, name):
    """Visualize data by category in a bar graph"""

    # Set the labels which are based on the keys of our counter.
    # labels needed to be utf-8 decoded, otherwise plt.xticks
    # broke with unicode-decode-error
    # tuple instead of list for performance?
    labels = tuple([i.decode('utf-8') for i in counter.keys()])

    outfolder = 'output'

    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    fullpath_outfile = "{0}/{1}.png".format(outfolder, name)

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
