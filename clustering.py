'''
Module in charge of grouping the samples according to their similarity.
'''
import random
def group_up(samples_matrix, id_samples, centers, clusters):
    '''Returns the elements grouped according to the similarity with the centers.'''
    for sample in range(len(id_samples)):
        if sample not in centers:
            current_cluster = 0
            best_cluster = current_cluster
            best_cluster_center = centers[0]
            for center in centers:
                if samples_matrix[sample][center] > samples_matrix[sample][best_cluster_center]:
                    best_cluster_center = center
                    best_cluster = current_cluster
                current_cluster += 1
            distance_sample = (id_samples[sample], samples_matrix[sample][best_cluster_center])
            clusters[best_cluster].append(distance_sample)
    return clusters

def calc_next_centers(clusters, id_samples, samples_matrix):
    '''Function in charge of calculating the centers of each cluster.'''
    centers = []
    for cluster in clusters:
        best_distance = cluster[0][1]
        new_center = 0
        for i in range(len(cluster)):
            sum_distances = 0
            sample_index = id_samples.index(cluster[i][0])
            for j in range(len(cluster)):
                if i != j:
                    index = id_samples.index(cluster[j][0])
                    sum_distances += samples_matrix[sample_index][index]
            if best_distance == 0 or best_distance < sum_distances:
                best_distance = sum_distances
                new_center = sample_index
        centers.append(new_center)
    return centers

def compare_clusters(current_clusters, last_clusters):
    '''This function compares if two cluster groups are equal.'''
    if len(current_clusters) != len(last_clusters):
        return False
    for cluster in range(len(current_clusters)):
        if len(current_clusters[cluster]) != len(last_clusters[cluster]):
            return False
        for sample in range(len(current_clusters[cluster])):
            current_cluster = current_clusters[cluster][sample][0]['sample']
            if current_cluster != last_clusters[cluster][sample][0]['sample']:
                return False
    return True

def k_medoids(samples_matrix, id_samples, k=3):
    '''Function in charge of grouping the samples according to their similarity.'''
    #select the init centers clusters
    iterations = 0
    centers = random.sample(range(len(id_samples)), k)
    clusters = [[(id_samples[i], samples_matrix[i][i])] for i in centers]
    clusters = group_up(samples_matrix, id_samples, centers, clusters)
    last_clusters = []
    while not compare_clusters(clusters, last_clusters):
        iterations += 1
        centers = calc_next_centers(clusters, id_samples, samples_matrix)
        last_clusters = clusters
        clusters = [[(id_samples[i], samples_matrix[i][i])] for i in centers]
        clusters = group_up(samples_matrix, id_samples, centers, clusters)
    #delete distance to metoids of all clusters
    end_clusters = []
    for cluster in clusters:
        end_cluster = []
        for sample in cluster:
            end_cluster.append(sample[0])
        end_clusters.append(end_cluster)
    return end_clusters
