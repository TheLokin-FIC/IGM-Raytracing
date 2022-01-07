import numpy as np

from primitives.vector import normalize


class Sphere():
    def __init__(self, center, radius, color):
        self.center = np.array(center)
        self.radius = radius
        self.color = np.array(color)

    def intersect(self, O, D):
        # Return the distance from O to the intersection of the ray (O, D) with the
        # sphere (S, R), or +inf if there is no intersection.
        # O (origin) and S (center) are 3D points, D (direction) is a normalized
        # vector, R (radius) is a scalar.

        a = np.dot(D, D)
        OS = O - self.center
        b = 2 * np.dot(D, OS)
        c = np.dot(OS, OS) - self.radius * self.radius
        disc = b * b - 4 * a * c
        if disc > 0:
            distSqrt = np.sqrt(disc)
            q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
            t0 = q / a
            t1 = c / q
            t0, t1 = min(t0, t1), max(t0, t1)
            if t1 >= 0:
                return t1 if t0 < 0 else t0

        return np.inf

    def normal_at(self, point):
        return normalize(point - self.center)

    def color_at(self, point):
        return self.color

    def get_diffuse(self):
        return 1.0

    def get_specular(self):
        return 1.0

    def get_reflection(self):
        return 0.5
