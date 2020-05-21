#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
import preprocesamiento
import ctypes

def get_arn_string(content):
    content = content.decode('utf-8')
    arn_string = content[content.find('\n') + 1:]
    return arn_string

def load_arn_samples(samples):
   samples_id_list = []
   if not os.path.exists('samples/'):
      os.mkdir('samples/')
   for sample in samples:
      id = sample[0]
      samples_id_list.append(id)
      sample_path = 'samples/{0}.fasta'.format(id)
      if not os.path.exists(sample_path):
         url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id={0}&rettype=fasta".format(id)
         sample_content = requests.get(url).content
         arn_string = get_arn_string(sample_content)   
         print('Descargando muestra {0}'.format(id))
         with open(sample_path, 'a') as sample_file:
            sample_file.write(arn_string)
            sample_file.close()
   return samples_id_list

#ALGORITM: Needleman–Wunsch
def calcNeedlemanScore(seq1, seq2, max_len):
    needlemanScore = ctypes.CDLL('library/alineamiento.so')
    needlemanScore.calc_needleman_score.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_int,ctypes.POINTER(ctypes.c_char), ctypes.c_int,)
    needlemanScore.calc_needleman_score.restype = ctypes.c_int 
    len_seq1 = len(seq1) if len(seq1) < max_len else max_len
    len_seq2 = len(seq2) if len(seq2) < max_len else max_len
    seq1_array = ctypes.c_char * len_seq1
    seq2_array = ctypes.c_char * len_seq2
    n = ctypes.c_int(len_seq1)
    m = ctypes.c_int(len_seq2) 
    return needlemanScore.calc_needleman_score(seq1_array(*seq1[:len_seq1].encode()),n,seq2_array(*seq2[:len_seq2].encode()),m)


def get_arn_sample(sample_id):
   try:
      sample_file = open('samples/{0}.fasta'.format(sample_id), 'r')
      sample = ''
      for line in sample_file:
         sample += line.split('\n')[0]
      return sample
   except:
      print('Error al cargar muestra')
     
def get_scores(samples, max_len = 1000):
    samples = load_arn_samples(samples)
    scores = []
    for i in range(len(samples)):
        sample_scores = []
        current_arn_str = get_arn_sample(samples[i])
        for j in range(len(samples)):
            if j < i:
                sample_scores.append(scores[j][i])
            else:
                arn_str_to_cmp = get_arn_sample(samples[j])
                sample_scores.append(calcNeedlemanScore(current_arn_str, arn_str_to_cmp, max_len))
        scores.append(sample_scores)
    return scores



            








