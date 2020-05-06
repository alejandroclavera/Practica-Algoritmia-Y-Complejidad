import csv


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


def quick_sort(sequence_samples, sequence):
   less = []
   pivotlist = []
   more = []
   if len(sequence_samples) <=1:
      return sequence_samples
   else:
      pivot_pos = len(sequence_samples)//2
      pivot = sequence[sequence_samples[pivot_pos]].get('Length')
      for i in sequence_samples:
         if sequence[i].get('Length') < pivot:
            less.append(i)
         elif sequence[i].get('Length') > pivot:
            more.append(i)
         else:
            pivotlist.append(i)
      less = quick_sort(less,sequence)
      more = quick_sort(more,sequence)
      return less + pivotlist + more

