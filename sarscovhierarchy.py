import preprocesamiento
import alineamiento
import clustering

def main():
    samples = preprocesamiento.get_median_samples_of_csv('sequences.csv')
    scores = alineamiento.get_scores(samples, max_len= 500)
    clusters, iterations, centers = clustering.k_metoids(scores, samples, k = 3)
    cluster_num = 1
    for cluster in clusters:
        print('-----------cluster {0}-----------'.format(cluster_num))
        for sample in cluster:
            print('-{0}'.format(sample[0][1]))
        cluster_num += 1
        

main()
    