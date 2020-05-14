#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
import requests
import os
import preprocesamiento
import ctypes

import threading
import math
import numpy


scoreMatrix = []

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

def get_arn_sample(sample_id):
   try:
      sample_file = open('samples/{0}.fasta'.format(sample_id), 'r')
      sample = ''
      for line in sample_file:
         sample += line.split('\n')[0]
      return sample
   except:
      print('Error al cargar muestra')

def generateRangeScores(iniVal, endVal):
   global scoreMatrix
   print("INI: "+str(iniVal)+" END: "+str(endVal))
   alreadyDone = iniVal
   for sample in range(alreadyDone,endVal+1):
      arn_str1 = get_arn_sample(samples[sample])
      for i in range(alreadyDone,len(scoreMatrix)):
         scoreMatrix[alreadyDone-1][i] = i#calcNeedlemanScore(arn_str1, get_arn_sample(samples[i]))
      alreadyDone += 1
   print("end")

def printMatrix(M):
    for r in M:
        for c in r:
            print(c, end=" ")
        print()


samples = load_arn_samples('sequences.csv')    
arn_str1 = get_arn_sample(samples[2][:1000])
arn_str12 = get_arn_sample(samples[4][:1000])
#print(calcNeedlemanScore(arn_str1,arn_str12))
#scoreMatrix = [[0 for x in range(len(samples))] for y in range(len(samples))]
scoreMatrix = [[0 for x in range(35)] for y in range(35)] 
generateRangeScores(1,35)
a = numpy.asarray(scoreMatrix)
numpy.savetxt("matrix.csv", a, delimiter=",")
#DEBUG
printMatrix(scoreMatrix)











#------------------------------CEMENTERIO------------------------------------
#print(calcNeedlemanScore("ATATAGC","ATATGC"))
#print(calcNeedlemanScore("GCATG-CA","G-ATTACA"))

#calcNeedlemanScore(arn_str1, arn_str12)
#generateScoreMatrix(35)


'''
if i == numOfThreads:
   endRang=35#len(samples)
else:
   endRang=2*i*calcRange
'''



'''
def test():
   arn_str1 = get_arn_sample(samples[2][:1000])
   arn_str12 = get_arn_sample(samples[4][:1000])
   print(calcNeedlemanScore(arn_str1,arn_str12))

thread1 = threading.Thread(target=test())
thread2 = threading.Thread(target=test())
thread1.setDaemon(True)
'''



'''
def generateScoreMatrix(numOfThreads): 
   threads = [] 
   #calcRange = math.ceil(35/numOfThreads)
   calcRange = 35//numOfThreads
   lastNum = calcRange + (35 - calcRange*numOfThreads)
   pivot = 1
   for i in range(1,numOfThreads+1):
      if i == numOfThreads:
         endRang=lastNum
      else:
         endRang=i*calcRange
      thread = threading.Thread(target=generateRangeScores(pivot,endRang))
      thread.setDaemon(True)
      threads.append(thread)
      pivot = endRang
   #Start
   for i in range(numOfThreads):
      threads[i].start()
   #Wait for threads
   for i in range(numOfThreads):
      threads[i].join()
'''