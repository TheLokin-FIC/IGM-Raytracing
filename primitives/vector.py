import numpy as np


def normalize(vector):
    return vector / np.linalg.norm(vector)


def reflect(vector, normal):
    return vector - 2 * vector.dot_product(normal) * normal
