import numpy as np

from primitives.vector import normalize


class Triangle():
    # Define the 3 vertices of the triangle in counter-clockwise order
    def __init__(self, v0, v1, v2, color):
        self.v0 = np.array(v0)
        self.v1 = np.array(v1)
        self.v2 = np.array(v2)
        self.color = np.array(color)

        self.edge0 = self.v1 - self.v0
        self.edge1 = self.v2 - self.v1
        self.edge2 = self.v0 - self.v2

        self.normal = normalize(np.cross(self.v1 - self.v0, self.v2 - self.v0))
        self.D = np.dot(self.normal, self.v0)

    def intersect(self, O, D):
        # Dot product of the triangle's normal and the ray's direction.
        product = np.dot(self.normal, D)

        # The dot product of two perpendicular vectors is 0,
        # so if the ray and the plane are parallel they wont intersect.
        if product == 0:
            return np.inf

        # Distance from the ray origin O to P.
        t = - (np.dot(self.normal, O) + self.D) / product

        # Check if the triangle is behind the ray.
        if t < 0:
            return np.inf

        # Compute intersection point with ray parametric equation.
        P = O + t * D
        C0 = np.cross(self.edge0, P - self.v0)
        C1 = np.cross(self.edge1, P - self.v1)
        C2 = np.cross(self.edge2, P - self.v2)

        # Check if P is inside the triangle
        if np.dot(self.normal, C0) < 0 or np.dot(self.normal, C1) < 0 or np.dot(self.normal, C2) < 0:
            return np.inf

        return t

    def normal_at(self, point):
        return self.normal

    def color_at(self, point):
        return self.color

    def get_diffuse(self):
        return 1.0

    def get_specular(self):
        return 1.0

    def get_reflection(self):
        return 1.0
