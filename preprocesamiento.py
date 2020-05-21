#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv

def load_regions(path):
   with open(path, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      next(csv_reader)
      locations = {}
      for row in csv_reader:
         locations[row['Geo_Location'].split(':')[0]] = {}
   return locations

def load_samples_of_csv(path):
   with open(path, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      next(csv_reader)
      samples = load_regions(path)
      for row in csv_reader:
         samples[row['Geo_Location'].split(':')[0]][row['Accession']] = {'Length':int(row['Length'])}      
   return samples

def quick_sort(list_to_sort):
   less = []
   pivotlist = []
   more = []
   if len(list_to_sort) <=1:
      return list_to_sort
   else:
      pivot_pos = len(list_to_sort) // 2
      pivot = list_to_sort[pivot_pos]
      for i in list_to_sort:
         if i[1] < pivot[1]:
            less.append(i)
         elif i[1] > pivot[1]:
            more.append(i)
         else:
            pivotlist.append(i)
      less = quick_sort(less)
      more = quick_sort(more)
      return less + pivotlist + more

def median(samples):
   lengths = [(sample,samples[sample]['Length'],sample) for sample in samples.keys()]
   return calculateMedian(lengths)[0] #get id of sample

def calculateMedian(lengths):
   return quickSelect(lengths, len(lengths) // 2)

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
      if element[1] < pivot[1]:
         smallerThan.append(element)
      elif element[1] > pivot[1]:
          biggerThan.append(element)
      else:
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
         sortedGroup = quick_sort(group)
         #Get medians of group
         medians.append(sortedGroup[2])
   #Median of medians
   return calculateMedian(medians)
   
def makeGroups(lisT, groupSize):
   return [lisT[i:i + groupSize] for i in range(0, len(lisT), groupSize)]

def basicMedian(lisT):
   lisT = quick_sort(lisT)
   return lisT[len(lisT) // 2]
   
def get_median_samples_of_csv(path):
   try:
      samples = load_samples_of_csv(path)
      median_samples = []
      for country in samples.keys():
         median_samples.append((median(samples[country]), country))
   except:
      raise Exception('ERROR => No se ha podigo cargar las muestras')
   return median_samples



