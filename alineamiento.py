#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This module gets the optimal alignment of each sequence compared to all the others.
'''
import os
import ctypes
import requests
def get_arn_string(content):
    '''This function removes the first line of the FASTA file'''
    content = content.decode('utf-8')
    arn_string = content[content.find('\n') + 1:]
    return arn_string

def load_arn_samples(samples):
    '''Downloads the samples and stores them in a file if they do not exist.'''
    samples_id_list = []
    if not os.path.exists('samples/'):
        os.mkdir('samples/')
    for sample in samples:
        sample_id = sample['sample']
        samples_id_list.append(sample_id)
        sample_path = 'samples/{0}.fasta'.format(sample_id)
        if not os.path.exists(sample_path):
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id={0}&rettype=fasta".format(sample_id)
            sample_content = requests.get(url).content
            arn_string = get_arn_string(sample_content)
            print('Descargando muestra {0}'.format(sample_id))
            with open(sample_path, 'a') as sample_file:
                sample_file.write(arn_string)
                sample_file.close()
    return samples_id_list

#ALGORITM: Needleman–Wunsch
def calc_needleman_score(seq1, seq2, max_len):
    '''Needleman – Wunsch algorithm implementation in c.'''
    needleman_score = ctypes.CDLL('library/alineamiento.so')
    needleman_score.calc_needleman_score.argtypes = (
        ctypes.POINTER(ctypes.c_char), ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.c_int,)
    needleman_score.calc_needleman_score.restype = ctypes.c_int
    len_seq1 = len(seq1) if len(seq1) < max_len else max_len
    len_seq2 = len(seq2) if len(seq2) < max_len else max_len
    seq1_array = ctypes.c_char * len_seq1
    seq2_array = ctypes.c_char * len_seq2
    seq1 = seq1_array(*seq1[:len_seq1].encode())
    seq2 = seq2_array(*seq2[:len_seq2].encode())
    len_seq1 = ctypes.c_int(len_seq1)
    len_seq2 = ctypes.c_int(len_seq2)
    return needleman_score.calc_needleman_score(seq1, len_seq1, seq2, len_seq2)

def get_arn_sample(sample_id):
    '''This function eliminates the line breaks of each sample read from the FASTA file.'''
    sample_file = open('samples/{0}.fasta'.format(sample_id), 'r')
    sample = ''
    for line in sample_file:
        sample += line.split('\n')[0]
    return sample

def get_scores(samples, max_len=1000):
    '''This function performs the alignment of all the RNA chains.'''
    samples = load_arn_samples(samples)
    scores = [[0 for j in range(len(samples))] for i in range(len(samples))]
    current_col = 0
    current_row = 0
    for sample in samples:
        current_arn_str = get_arn_sample(sample)
        current_col = current_row + 1
        for sample_to_aling in samples[current_row + 1:]:
            arn_str_to_cmp = get_arn_sample(sample_to_aling)
            score = calc_needleman_score(current_arn_str, arn_str_to_cmp, max_len)
            scores[current_row][current_col] = score
            scores[current_col][current_row] = score
            current_col += 1
        current_row += 1
    return scores
