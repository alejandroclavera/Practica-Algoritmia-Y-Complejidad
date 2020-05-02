#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import csv
import statistics

def load_regions(path):
   with open(path, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      next(csv_reader)
      locations = {}
      for row in csv_reader:
         locations[row['Geo_Location']] = {}
   return locations

def load_samples_of_csv(path):
   with open(path, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      next(csv_reader)
      samples = load_regions(path)
      for row in csv_reader:
         if row['Length'] != '':
            samples[row['Geo_Location']][row['Accession']] = {'Length':int(row['Length'])}      
   return samples

def calculate_median(samples):
   lengths = []
   for sample in samples.values():
      lengths.append(sample['Length']) 
   return statistics.median(lengths)

samples = load_samples_of_csv('sequences.csv')
print(calculate_median(samples['Iran']))




