#!/usr/bin/env python
# coding=utf-8
"""
getdata.py

Downloads datafiles from provided links into folder 'sourcedata'.
If 'sourcedata' does not exist, it will be created.
"""
import urllib
import os.path

datafolder = 'sourcedata'

files = [
  "http://datosabiertos.laspalmasgc.es/repositorio/policia/atestados/DB_ACC_2014.csv",
  "http://datosabiertos.laspalmasgc.es/repositorio/policia/atestados/DB_HER_2014.csv",
  "http://datosabiertos.laspalmasgc.es/repositorio/policia/atestados/DB_VEH_2014.csv"
]

if not os.path.exists(datafolder):
    os.mkdir(datafolder)

for file in files:
    filename = file.split('/')[-1]
    filepath = '{0}/{1}'.format(datafolder, filename)
    if not os.path.exists(filepath):
        urllib.urlretrieve(file, filepath)
