import random
import preprocesamiento
import alineamiento

def group_up(samples_matrix, id_samples,centers, clusters):
    for sample in range(len(id_samples)):
        if sample not in centers:
            current_cluster = 0
            best_cluster = current_cluster
            best_cluster_center = None
            for center in centers:
                if best_cluster_center == None:
                    best_cluster_center = center
                    best_cluster = current_cluster
                if samples_matrix[sample][center] < samples_matrix[sample][best_cluster_center]:
                    best_cluster_center = center
                    best_cluster = current_cluster
                current_cluster += 1
            clusters[best_cluster].append((id_samples[sample],samples_matrix[sample][sample]))
    return clusters

def calc_total_cost(clusters, centers):
    total_cost = 0
    for current_cluster in range(len(centers)):
        for sample in range(1,len(clusters[current_cluster])):
            total_cost += clusters[current_cluster][sample][1]
    return total_cost
            
def calc_next_centers(clusters):
    centers = []
    for cluster in clusters:
        centers.append(preprocesamiento.calculateMedian(cluster))
    return centers


def k_metoids(samples_matrix, id_samples, k=2):
    #select the init centers clusters
    iterations = 0
    centers = random.sample(range(len(id_samples)),k)
    clusters = [[(id_samples[i], samples_matrix[i][i])] for i in centers]
    clusters = group_up(samples_matrix, id_samples, centers, clusters)
    last_cost = 0
    current_cost = calc_total_cost(clusters,centers)
    while current_cost - last_cost > 0:
        iterations += 1
        centers = calc_next_centers(clusters)
        clusters = [[center] for center in centers]
        centers = [id_samples.index(center[0]) for center in centers]
        clusters = group_up(samples_matrix, id_samples, centers, clusters)
        last_cost = current_cost
        current_cost = calc_total_cost(clusters,centers)
    return clusters, iterations, centers
                  

scores, id= alineamiento.get_scores('sequences.csv')
print(k_metoids(scores, id, k=3))




    
        
    


