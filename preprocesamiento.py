import csv
from collections import OrderedDict
from operator import getitem

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
         samples[row['Geo_Location']][row['Accession']] = {'Length':int(row['Length'])}      
   return samples

<<<<<<< HEAD
def quick_sort(sequence):
   less = []
   pivotlist = []
   more = []
   if len(sequence) <=1:
      return sequence
   else:
      pivot = sequence[0]
      for i in sequence:
         if i < pivot:
            less.append(i)
         elif i > pivot:
            more.append(i)
         else:
            pivotlist.append(i)
      less = quick_sort(less)
      more = quick_sort(more)
      return less + pivotlist + more

def sort_dictionary(samples):
   print(samples)
   #samples.sort(key=operator.itemgetter(['Length']))
   #samples_sorted = {k: v for k, v in sorted(samples.items(), key=lambda x:x['Length'])}
   #print(samples)
   print(samples['Length'].values())
   #a = OrderedDict(sorted(samples.items(), key = lambda x: getitem(int(x[1]),'Length')))
   #print(a)

      #print(i, samples[i])
samples = open_csv('sequences.csv')
=======
#test

samples = load_samples_of_csv('sequences.csv')

>>>>>>> preprocesamiento

print(list(samples['Hong Kong'].keys()))
#a = [4,65,2,0,99,83,678,23]
print((list(samples['Hong Kong'].values())))
#x = open_csv('sequences.csv')
print(sort_dictionary(samples))
#print(samples['Spain']['MT359865']['Length'])
#print(samples['Hong Kong'])




