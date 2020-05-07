#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import csv
import random

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
   #Calculate median depending whether length is even or not
   if len(lengths) % 2 == 1:
      return quickSelect(lengths, len(lengths) / 2)
   else:
      return 0.5 * (quickSelect(lengths, len(lengths) / 2 - 1) + quickSelect(lengths, len(lengths) / 2))

def quickSelect(lengths,k):
   if len(lengths) == 1:
      return lengths[0]
   else:
      smallerThan, biggerThan, equalTo = partition(lengths)
      if k < len(smallerThan):
         return quickSelect(smallerThan,k)
      elif k < len(smallerThan) + len(equalTo):     
         #Median found
         return equalTo[0]
      else:
         return quickSelect(biggerThan,k-len(smallerThan)-len(equalTo))

def partition(partitionList):
   pivot = random.choice(partitionList) 
   smallerThan = []
   biggerThan = []
   equalTo = []
   #Smaller than the pivot
   for element in partitionList:
      if element < pivot:
         smallerThan.append(element)
   #Bigger than the pivot
   for element in partitionList:
      if element > pivot:
         biggerThan.append(element)
   #Equal to the pivot
   for element in partitionList:
      if element == pivot:
         equalTo.append(element)
   return smallerThan, biggerThan, equalTo


samples = load_samples_of_csv('sequences.csv')
for country in samples:
   print(calculate_median(samples[country]))




