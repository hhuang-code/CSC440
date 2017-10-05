"""
Used in ex 2.8
In python terminal, type "from dist import *"
"""

import math

#Return the magnitude of a vector
def magnitude(vector):
    return math.sqrt(sum(vector[i] * vector[i] for i in range(len(vector))))

#Return the normalization form of a vector
def normform(vector):
    mag = magnitude(vector)
    return [vector[i] / mag  for i in range(len(vector))]

# Return the cosine distance of two vectors
def cosdist(vector1, vector2):
    dot_prod = sum(vector1[i] * vector2[i] for i in range(len(vector1)))
    return dot_prod / (magnitude(vector1) * magnitude(vector2))

# Return the Euclidean distance of two vectors
def edist(vector1, vector2):
    return math.sqrt(sum((vector1[i] - vector2[i]) ** 2 for i in range(len(vector1))))
