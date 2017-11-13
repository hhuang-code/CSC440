import numpy as np
import sys
import random

# Load dataset
def readin(filename = 'kdata'):
    dataset = []
    # Read in file. Each line is a point
    with open(filename) as f:
        for line in f:
            co_arr = line.strip().split(',')
            dims = len(co_arr)
            pt = []
            # Add each dim to the point
            for i in range(dims):
                pt.append(float(co_arr[i]))
            # Add each point to the dataset
            dataset.append(pt)
    return dataset

# Calculate distance between two point
def cal_dist(pt1, pt2):
    dims = len(pt1)
    dist = 0.0
    for i in range(dims):
        dist += (pt1[i] - pt2[i]) ** 2
    return np.sqrt(dist)

# Given a tuple set, Calculate the mean tuple
def cal_mean(tset):
    mean = []
    cnt = 0
    for pt in tset:
        if len(mean) == 0:
            mean = np.asarray(pt)
        else:
            mean = np.add(mean, pt)
        cnt += 1

    return mean / cnt

# Get the sub dataset which exculdes centers
def get_candidate(centers, dataset):
    ca = list(dataset)
    for center in centers:
        ca.remove(center)
    return ca

# For every element in non-center set, calculate the
# shortest distance from a data point to the closest center
def cal_min_dist(centers, ca):
    min_dist_arr = []
    for pt in ca:
        min_dist = sys.float_info.max
        for center in centers:
            dist = cal_dist(pt, center)
            if dist < min_dist:
                min_dist = dist
        min_dist_arr.append(min_dist)

    return min_dist_arr

# Use the shortest distance to generate the probability to be selected
def gen_prob(min_dist_arr):
    weight = [x ** 2 for x in min_dist_arr]
    weight = [float(x) / sum(weight) for x in weight]
    return weight

# Generate initial k centers
def gen_ini_centers(k, dataset):
    ini_centers = []
    # Randomly choose the first center
    first_center = dataset[random.randint(0, k - 1)]
    ini_centers.append(first_center)
    # Generate the remaining centers
    while len(ini_centers) < k:
        ca = get_candidate(ini_centers, dataset)
        min_dist_arr = cal_min_dist(ini_centers, ca)
        prob = gen_prob(min_dist_arr)
        idx_arr = list(range(len(ca)))
        center_idx = (np.random.choice(idx_arr, 1, False, prob))[0]
        ini_centers.append(ca[center_idx])

    return ini_centers

# Initialize k-means clusters
def ini_clustering(ini_centers, dataset):
    clusters = {}
    k = len(ini_centers)
    for i in range(k):
        center = ini_centers[i]
        # For each center, create a set to store points
        clusters[tuple(center)] = set()
        # Add the initial center to the set
        clusters[tuple(center)].add(tuple(center))
    return clusters

# Cluster process: given previous clusters, and return new clusters
def clustering(pre_clusters, dataset):
    sample_num = len(dataset)
    # clear all cluster sets in pre_clusters
    for center in pre_clusters:
        pre_clusters[center].clear()

    for i in range(sample_num):
        min_dist = sys.float_info.max
        assign_center = tuple()
        for center in pre_clusters:
            dist = cal_dist(dataset[i], center)
            if dist < min_dist:
                min_dist = dist
                assign_center = center
        # Assign the point to the new center
        pre_clusters[assign_center].add(tuple(dataset[i]))

    # Calculate new centers by mean
    for center in pre_clusters:
        new_center = cal_mean(pre_clusters[center])
        # Add new center and delete previous center
        pre_clusters[tuple(new_center)] = pre_clusters.pop(center)

    return pre_clusters

def main():
    dataset = readin()
    k = 3
    # Choose initial centers
    ini_centers = gen_ini_centers(k, dataset)
    print('Initial center: ', ini_centers)

    # Initialize clusters. Only the center in each cluster
    ini_clusters = ini_clustering(ini_centers, dataset)

    new_clusters = clustering(ini_clusters, dataset)
    pre_clusters = new_clusters
    new_clusters = clustering(pre_clusters, dataset)
    #while not check_same(pre_clusters, new_clusters):
    while pre_clusters != new_clusters:
        pre_clusters = new_clusters
        new_clusters = clustering(pre_clusters)

    # The final three clusters
    print('Final three clusters:')
    new_clusters = clustering(ini_clusters, dataset)
    for center in new_clusters:
        print('Center: ', center, ' Clusters: ', new_clusters[center])
    print()

if __name__ == '__main__':
    main()

