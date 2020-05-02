import csv

def load_locations(path):
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
      samples = load_locations(path)
      for row in csv_reader:
         samples[row['Geo_Location']][row['Accession']] = {'Length':row['Length']}      
   return samples
                  
samples = load_samples_of_csv('sequences.csv')



