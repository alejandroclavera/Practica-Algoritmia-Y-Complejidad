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

#test

samples = load_samples_of_csv('sequences.csv')




