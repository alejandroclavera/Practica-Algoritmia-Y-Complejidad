#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Esta script prepara las mustras leidas del csv, para su posterior tratamiento.
'''
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
            length = {'Length':int(row['Length'])}
            samples[row['Geo_Location'].split(':')[0]][row['Accession']] = length
    return samples

def quick_sort(list_to_sort):
    less = []
    pivotlist = []
    more = []
    if len(list_to_sort) <= 1:
        return list_to_sort
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
    lengths = [(sample, samples[sample]['Length']) for sample in samples.keys()]
    return calculate_median(lengths) #get id of sample

def calculate_median(lengths):
    sorted_lengths = quick_sort(lengths)
    return sorted_lengths[len(sorted_lengths) // 2]

def get_median_samples_of_csv(path):
    samples = load_samples_of_csv(path)
    median_samples = []
    for country in list(samples.keys()):
        median_sample = median(samples[country])[0]
        median_samples.append({'country':country, 'sample':median_sample})
    return median_samples
