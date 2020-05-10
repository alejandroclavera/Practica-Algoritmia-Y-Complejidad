#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
import requests
import os
import preprocesamiento

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

load_arn_samples('sequences.csv')  



#ALGORITM: Needleman–Wunsch
similarityMatrix = [[10,-1,-3,-4],[-1,7,-5,-3],[-3,-5,9,0],[-4,-3,0,8]]
gapPenalty = -5 
charIndx = {
    "A":0,
    "G":1,
    "C":2,
    "T":3,
}

def calcSimil(a,b):
    if a == '-' or b == '-':
        return gapPenalty
    else:
        return similarityMatrix[charIndx[a]][charIndx[b]]

def calcNeedlemanScore(seq1, seq2):
    M = []
    n = len(seq1)
    m = len(seq2)
    M = [[0 for x in range(n+1)] for y in range(m+1)] 
    #Base cases
    for i in range(m+1):
        M[i][0] = gapPenalty*i
    for j in range(n+1):
        M[0][j] = gapPenalty*j
    #Calculate diagonal cost
    for i in range(1, m+1):
        for j in range(1, n+1):
            Match = M[i-1][j-1] + calcSimil(seq1[j-1],seq2[i-1])
            Delete = M[i-1][j] + gapPenalty
            Insert = M[i][j-1] + gapPenalty
            M[i][j] = max(Match,Delete,Insert)
    #Align words
    align1 = ""
    align2 = ""
    i = m
    j = n
    while i > 0 and j > 0:
        if M[i][j] == M[i-1][j-1] + calcSimil(seq1[j-1], seq2[i-1]):
            align1 += seq1[j-1]
            align2 += seq2[i-1]
            i -= 1
            j -= 1
        elif M[i][j] == M[i][j-1] + gapPenalty:
            align1 += seq1[j-1]
            align2 += '-'
            j -= 1
        elif M[i][j] == M[i-1][j] + gapPenalty:
            align1 += '-'
            align2 += seq2[i-1]
            i -= 1
    # Finish tracing up to the top left cell
    while j > 0:
        align1 += seq1[j-1]
        align2 += '-'
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i-1]
        i -= 1
    #Invert words because we started from the bottom left (debug only)
    '''
    align1 = align1[::-1]
    align2 = align2[::-1] 
    '''
    #Calculate score
    score = 0
    i = min(len(align1),len(align2))-1
    while i >= 0:
        score += calcSimil(align1[i],align2[i])
        i -= 1
    return score

#Debug only
'''
def printMatrix(M):
    for r in M:
        for c in r:
            print(c, end=" ")
        print()
'''
#More score -> more similar
print(calcNeedlemanScore("ATATAGC","A"))

