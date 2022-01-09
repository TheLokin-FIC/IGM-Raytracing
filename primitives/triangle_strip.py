import numpy as np

from primitives.triangle import Triangle


class TriangleStip():
    def __init__(self, vectors, color):
        # Draws a series of triangles using vertices v0, v1, v2, then
        # v2, v1, v3, then v2, v3, v4, and so on.

        v0 = vectors.pop(0)
        v1 = vectors.pop(0)
        self.triangles = []
        for i in range(len(vectors)):
            v2 = vectors[i]
            if i % 2 == 0:
                self.triangles.append(Triangle(v0, v1, v2, color))
            else:
                self.triangles.append(Triangle(v1, v0, v2, color))
            v0 = v1
            v1 = v2

    def intersect(self, O, D):
        # Find first triangle of intersection with the scene.
        self.triangle = None
        t = np.inf

        for triangle in self.triangles:
            t_obj = triangle.intersect(O, D)
            if t_obj < t:
                self.triangle = triangle
                t = t_obj

        return t

    def normal_at(self, point):
        return self.triangle.normal_at(point)

    def color_at(self, point):
        return self.triangle.color_at(point)

    def get_diffuse(self):
        return self.triangle.get_diffuse()

    def get_specular(self):
        return self.triangle.get_specular()

    def get_reflection(self):
        return self.triangle.get_reflection()
