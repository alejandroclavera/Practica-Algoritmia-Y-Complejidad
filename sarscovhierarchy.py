'''
This program groups the samples obtained from the SARS-CoV-2 of a csv according to their similarity.
'''
import sys
import preprocesamiento
import alineamiento
import clustering
def main():
    '''Program execution.'''
    if len(sys.argv) < 2:
        print('sarscovhierachy <sequences_path>')
        sys.exit(0)
    try:
        sequences_path = sys.argv[1]
        samples = preprocesamiento.get_median_samples_of_csv(sequences_path)
        print('MSG => Alineando las secuencias, esta operación puede tardar un poco.')
        scores = alineamiento.get_scores(samples, max_len=1000)
    except FileNotFoundError:
        print('ERROR => No se ha podido cargar las muestras')
        sys.exit(0)
    #create the clusters with k_medoids algorithm
    clusters = clustering.k_medoids(scores, samples, k=3)
    cluster_num = 1
    for cluster in clusters:
        print('-----------cluster {0}-----------'.format(cluster_num))
        for sample in cluster:
            print(dict(sample)['country'])
        cluster_num += 1
main()
    