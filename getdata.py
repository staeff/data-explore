#!/usr/bin/env python
# coding=utf-8

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
    filename = '{0}/{1}'.format(datafolder, file.split('/')[-1])
    print filename
    # urllib.urlretrieve(file, filename)
