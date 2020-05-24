import random
import preprocesamiento
import alineamiento
import sys

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
            clusters[best_cluster].append((id_samples[sample],samples_matrix[sample][best_cluster_center]))
    return clusters

def calc_total_cost(clusters, centers):
    total_cost = 0
    for current_cluster in range(len(centers)):
        for sample in range(1,len(clusters[current_cluster])):
            total_cost += clusters[current_cluster][sample][1]
    return total_cost
            
def calc_next_centers(clusters, id_samples, samples_matrix):
    centers = []
    for cluster in clusters:
        best_distance = cluster[0][1]
        new_center = id_samples.index(cluster[0][0])
        for i in range(len(cluster)):
            sum_distances = 0 
            sample_index = id_samples.index(cluster[i][0])
            for j in range(len(cluster)):
                if i != j:
                    index = id_samples.index(cluster[j][0])
                    sum_distances += samples_matrix[sample_index][index]
            if best_distance > sum_distances:
                best_distance = sum_distances
                new_center = sample_index
        centers.append(new_center)          
    return centers

def compare_clusters(current_clusters, last_clusters):
    if len(current_clusters) != len(last_clusters):
        return False
    for cluster in range(len(current_clusters)):
        if len(current_clusters[cluster]) != len(last_clusters[cluster]):
            return False
        else:
            for sample in range(len(current_clusters[cluster])):
                if current_clusters[cluster][sample][0][0] != last_clusters[cluster][sample][0][0]:
                    return False
    return True
        
def k_metoids(samples_matrix, id_samples, k=3, test_mode = False):
    #select the init centers clusters
    iterations = 0
    centers = random.sample(range(len(id_samples)),k)
    clusters = [[(id_samples[i], samples_matrix[i][i])] for i in centers]
    clusters = group_up(samples_matrix, id_samples, centers, clusters)
    last_cost = 0
    last_clusters = []
    current_cost = calc_total_cost(clusters,centers)
    while not compare_clusters(clusters, last_clusters) > 0:
        iterations += 1
        centers = calc_next_centers(clusters, id_samples, samples_matrix)
        last_clusters = clusters
        clusters = [[(id_samples[i], samples_matrix[i][i])] for i in centers]
        clusters = group_up(samples_matrix, id_samples, centers, clusters)
        last_cost = current_cost
        current_cost = calc_total_cost(clusters,centers)

    if test_mode:
        return clusters, iterations, centers
    else:
        #delete distance to metoids of all lusters
        for i in range(len(clusters)):
            for j in range(len(clusters[i])):
                clusters[i][j] = clusters[i][j][0]
        return clusters





    
        
    


