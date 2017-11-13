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

# Generate a random integer between [0, k)
def gen_random(k):
    rand = random.randint(0, k - 1)
    return rand

# Calculate distance between two point
def cal_dist(pt1, pt2):
    dims = len(pt1)
    dist = 0.0
    for i in range(dims):
        dist += (pt1[i] - pt2[i]) ** 2
    return np.sqrt(dist)

# Calculate the absolute error. Clusters are stored in a hashtable
def cal_abs_err(clusters):
    abs_err = 0
    for center in clusters:
        for pt in clusters[center]:
            abs_err += cal_dist(center, pt)
    return abs_err

# Initialize k-medoids clusters
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

# Assign process: given center index, assign all points and return new clusters
def clustering(centers, dataset):
    clusters = {}
    k = len(centers)
    for i in range(k):
        center = centers[i]
        # For each center, create a set to store points
        clusters[tuple(center)] = set()

    # Assign each sample point to the closest center
    sample_num = len(dataset)
    for i in range(sample_num):
        min_dist = sys.float_info.max
        assign_center = tuple()
        for center in clusters:
            dist = cal_dist(dataset[i], center)
            if dist < min_dist:
                min_dist = dist
                assign_center = center
        # Assign the point to the closest center
        clusters[assign_center].add(tuple(dataset[i]))

    return clusters

def main():
    dataset = readin()
    ini_center_idx = [0, 3, 6]
    # Initialize clusters. Only the center in each cluster
    ini_centers = []
    for i in range(len(ini_center_idx)):
        ini_centers.append(dataset[ini_center_idx[i]])

    # ini_clusters = ini_clustering(ini_centers, dataset)
    # The first round of execution
    new_clusters = clustering(ini_centers, dataset)
    print(cal_abs_err(new_clusters))
    
    sample_num = len(dataset)
    pre_centers = ini_centers
    pre_clusters = new_clusters
    while True:
        pre_abs_err = cal_abs_err(pre_clusters)
        k = len(pre_centers)
        min_centers = []
        min_clusters = {}
        min_abs_err = sys.float_info.max
        for i in range(k):
            tmp_centers = pre_centers
            # Change a center with a random number
            rand = gen_random(sample_num)
            while dataset[rand] in tmp_centers:
                rand = gen_random(sample_num)
            tmp_centers[i] = dataset[rand]
            tmp_clusters = clustering(tmp_centers, dataset)
            tmp_abs_err = cal_abs_err(tmp_clusters)
            if tmp_abs_err < min_abs_err:
                # Update centers and absolute errors
                min_centers = tmp_centers
                min_clusters = tmp_clusters
                min_abs_err = tmp_abs_err

        # Choose the clusters with minimal error as new clusters
        if min_abs_err < pre_abs_err:
            new_centers = min_centers
            new_clusters = min_clusters

        #if check_same(pre_clusters, new_clusters):
        if pre_clusters == new_clusters:
            break
        else:
            pre_clusters = new_clusters

    # The final three clusters
    print('Final three clusters:')
    for center in new_clusters:
        print('Center: ', center, ' Clusters: ', new_clusters[center])
    print()

if __name__ == '__main__':
    main()
