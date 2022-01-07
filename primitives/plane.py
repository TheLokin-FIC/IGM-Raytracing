import numpy as np

from primitives.vector import normalize


class Plane():
    def __init__(self, position, normal):
        self.position = np.array(position)
        self.normal = np.array(normal)

    def intersect(self, O, D):
        # Return the distance from O to the intersection of the ray (O, D) with the
        # plane (P, N), or +inf if there is no intersection.
        # O (origin) and P (position) are 3D points, D (direction) and N (normal)
        # are normalized vectors.

        denom = np.dot(D, self.normal)
        if np.abs(denom) < 1e-6:
            return np.inf

        d = np.dot(self.position - O, self.normal) / denom
        if d < 0:
            return np.inf

        return d

    def normal_at(self, point):
        return self.normal

    def color_at(self, point):
        return np.ones(3) if (int(point[0] * 2) % 2) == (int(point[2] * 2) % 2) else np.zeros(3)

    def get_diffuse(self):
        return 0.75

    def get_specular(self):
        return 0.5

    def get_reflection(self):
        return 0.25
