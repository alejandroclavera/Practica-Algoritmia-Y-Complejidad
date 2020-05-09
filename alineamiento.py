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
