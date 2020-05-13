#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
import requests
import os
import preprocesamiento
import ctypes

def get_arn_string(content):
    content = content.decode('utf-8')
    arn_string = content[content.find('\n') + 1:]
    return arn_string

def load_arn_samples(csv_path):
   samples = preprocesamiento.get_median_samples_of_csv(csv_path)
   samples_id_list = []
   if not os.path.exists('samples/'):
      os.mkdir('samples/')
   for sample in samples:
      id = sample[0]
      samples_id_list.append(id)
      sample_path = 'samples/{0}.fasta'.format(id)
      has_error = False
      error_list = []
      if not os.path.exists(sample_path):
         url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id={0}&rettype=fasta".format(id)
         sample_content = requests.get(url).content
         arn_string = get_arn_string(sample_content)   
         print('Descargando muestra {0}'.format(id))
         with open(sample_path, 'a') as sample_file:
            sample_file.write(arn_string)
            sample_file.close()
            if len(arn_string.replace('\n','')) != sample[1]:#provisional
               has_error = True
               error_list.append('{0} esperado = {1}, actual = {2}'.format(id, sample[1], len(arn_string.replace('\n',''))))
   if has_error:
      print('Error en las longitudes')
      for e in error_list:
         print(e)
   else:
      print('Se han cargado las muestras correctamente y no hay errores en las longitudes')
   return samples_id_list

#ALGORITM: Needleman–Wunsch
def calcNeedlemanScore(seq1, seq2):
    needlemanScore = ctypes.CDLL('library/alineamiento.so')
    needlemanScore.calc_needleman_score.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_int,ctypes.POINTER(ctypes.c_char), ctypes.c_int,)
    needlemanScore.calc_needleman_score.restype = ctypes.c_int 
    n = len(seq1)
    m = len(seq2)
    seq1_array = ctypes.c_char * n
    seq2_array = ctypes.c_char * m
    n = ctypes.c_int(n)
    m = ctypes.c_int(m) 
    return needlemanScore.calc_needleman_score(seq1_array(*seq1.encode()),n,seq2_array(*seq2.encode()),m)

samples = load_arn_samples('sequences.csv')
def get_arn_sample(sample_id):
   try:
      sample_file = open('samples/{0}.fasta'.format(sample_id), 'r')
      sample = ''
      for line in sample_file:
         sample += line.split('\n')[0]
      return sample
   except:
      print('Error al cargar muestra')
     
arn_str1 = get_arn_sample(samples[0])
arn_str12 = get_arn_sample(samples[1])
print(calcNeedlemanScore(arn_str1,arn_str12))






