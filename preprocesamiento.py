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

def median(samples):
   lengths = []
   for sample in samples.values():
      lengths.append(sample['Length']) 
   return calculateMedian(lengths)

def calculateMedian(lengths):
   #Calculate median depending whether length is even or not
   if len(lengths) % 2 == 1:
      return quickSelect(lengths, len(lengths) // 2)
   else:
      return 0.5 * (quickSelect(lengths, len(lengths) // 2 - 1) + quickSelect(lengths, len(lengths) // 2))

def quickSelect(lisT,k):
   if len(lisT) == 1:
      return lisT[0]
   else:
      smallerThan, biggerThan, equalTo = partition(lisT)
      if k < len(smallerThan):
         return quickSelect(smallerThan,k)
      elif k < len(smallerThan) + len(equalTo):     
         #Median found
         return equalTo[0]
      else:
         return quickSelect(biggerThan,k-len(smallerThan)-len(equalTo))

def partition(partitionList):
   pivot = pickPivot(partitionList) 
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

def pickPivot(lisT):
   #Algorith: median of medians
   assert len(lisT) > 0
   if len(lisT) < 5:
      return basicMedian(lisT)  
   #Separate into groups
   groups = makeGroups(lisT, 5)
   #Sort groups which size is equal to 5 and get their medians  
   medians = []
   for group in groups:
      if len(group) == 5:
         #Sort groups
         sortedGroup = sorted(group) #TODO change with quickSort
         #Get medians of group
         medians.append(sortedGroup[2])
   #Median of medians
   return calculateMedian(medians)
   
def makeGroups(lisT, groupSize):
   return [lisT[i:i + groupSize] for i in range(0, len(lisT), groupSize)]

def basicMedian(lisT):
   lisT = sorted(lisT)        #TODO change with quickSort
   if len(lisT) % 2 == 1:
      return lisT[len(lisT) // 2]
   else:
      return 0.5 * (lisT[len(lisT) // 2 - 1] + lisT[len(lisT) // 2])


samples = load_samples_of_csv('sequences.csv')
'''
for country in samples:
   print(calculate_median(samples[country]))
'''
print(median(samples['Iran']))



