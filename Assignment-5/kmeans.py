import numpy as np
import sys

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

# Initialize k-means clusters
def ini_clustering(ini_center_idx, dataset):
    clusters = {}
    k = len(ini_center_idx)
    for i in range(k):
        center = dataset[ini_center_idx[i]]
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

# Check whether two clusters are the same
def check_same(c1, c2):
    if len(c1) == len(c2):
        for center in c1:
            if c1[center] != c2[center]:
                return False
        return True
    else:
        return False

def main():
    dataset = readin()
    ini_center_idx = [0, 3, 6]
    # Initialize clusters. Only the center in each cluster
    ini_clusters = ini_clustering(ini_center_idx, dataset)
    
    # The first round of execution
    print('Three clusters after the first round of execution:')
    new_clusters = clustering(ini_clusters, dataset)
    for center in new_clusters:
        print('Center: ', center, ' Clusters: ', new_clusters[center])
    print()


    pre_clusters = new_clusters
    new_clusters = clustering(pre_clusters, dataset)
    while not check_same(pre_clusters, new_clusters):
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
