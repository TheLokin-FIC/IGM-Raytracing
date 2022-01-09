"""
MIT License

Copyright (c) 2017 Cyrille Rossant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from primitives.plane import Plane
from primitives.sphere import Sphere
from primitives.triangle import Triangle
from primitives.triangle_strip import TriangleStip
from primitives.vector import normalize

# Image dimensions
width = 400
height = 300

# Default light and material parameters.
ambient = 0.05
specular_k = 50

# Maximum number of light reflections.
depth_max = 5

# List of objects.
scene = [
    Plane([0.0, -0.5, 0.0], [0.0, 1.0, 0.0]),
    Sphere([0.75, 0.1, 1.0], 0.6, [0.0, 0.0, 1.0]),  # Blue
    Sphere([-0.75, 0.1, 2.25], 0.6, [0.5, 0.223, 0.5]),  # Purple
    Sphere([-2.75, 0.1, 3.5], 0.6, [1.0, 0.572, 0.184]),  # Orange
    Triangle([-0.5, -0.5, -0.5], [-1.0, -0.5, -0.5], [-1.0, 0.0, -0.5],
             [0.0, 1.0, 0.0]),
    Triangle([0.5, -0.5, 0.5], [0.5, 0.0, 1.0], [0.5, -0.5, 1.0],
             [1.0, 0.0, 0.0]),
    TriangleStip([
        [-0.76, 3.34, -5.0],
        [1.4, 2.9, -5.0],
        [-1.84, 2.26, -5.0],
        [2.0, 1.5, -5.0],
        [-1.84, 0.74, -5.0],
        [1.40, 0.1, -5.0],
        [-0.76, -0.34, -5.0],
    ], [0.0, 1.0, 1.0]),
]

# List of light positions and colors.
lights = [
    (np.array([5.0, 5.0, -10.0]), np.array([1.0, 1.0, 1.0])),  # White
    (np.array([-10.0, 5.0, 5.0]), np.array([1.0, 0.0, 1.0])),  # Red
]


def trace_ray(rayO, rayD):
    # Find first point of intersection with the scene.
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = obj.intersect(rayO, rayD)
        if t_obj < t:
            t, obj_idx = t_obj, i

    # Return None if the ray does not intersect any object.
    if t == np.inf:
        return

    # Find the object.
    obj = scene[obj_idx]

    # Find the point of intersection on the object.
    M = rayO + rayD * t

    # Find properties of the object.
    N = obj.normal_at(M)
    color = obj.color_at(M)
    toO = normalize(O - M)

    # Start computing the color.
    col_ray = ambient
    has_light = False
    for L, color_light in lights:
        toL = normalize(L - M)

        # Shadow: find if the point is shadowed or not.
        l = [obj_sh.intersect(M + N * 0.0001, toL)
             for k, obj_sh in enumerate(scene) if k != obj_idx]
        if not (l and min(l) < np.inf):
            has_light = True

        # Lambert shading (diffuse).
        col_ray += obj.get_diffuse() * max(np.dot(N, toL), 0) * color

        # Blinn-Phong shading (specular).
        col_ray += obj.get_specular() * max(np.dot(N, normalize(toL + toO)),
                                            0) ** specular_k * color_light
    if not has_light:
        return

    return obj, M, N, col_ray


# Camera view.
O = np.array([0.0, 0.35, -1.0])  # Camera.
Q = np.array([0.0, 0.0, 0.0])  # Camera pointing to.

# Screen coordinates (left, top, right, bottom): x0, y0, x1, y1.
ratio = width / height
S = (-1.0, -1.0 / ratio + 0.25, 1.0, 1.0 / ratio + 0.25)

# Loop through all pixels.
image = np.zeros((height, width, 3))
progress = tqdm(total=width * height)
for i, x in enumerate(np.linspace(S[0], S[2], width)):
    for j, y in enumerate(np.linspace(S[1], S[3], height)):
        col = np.zeros(3)
        reflection = 1.0

        Q = np.array([x, y, 0.0])
        D = normalize(Q - O)
        rayO, rayD = O, D

        # Loop through initial and secondary rays.
        for _ in range(depth_max):
            traced = trace_ray(rayO, rayD)
            if not traced:
                break
            obj, M, N, col_ray = traced

            # Reflection: create a new ray.
            rayO, rayD = M + N * \
                0.0001, (normalize(rayD - 2 * np.dot(rayD, N) * N))

            col += reflection * col_ray
            reflection *= obj.get_reflection()

        image[height - 1 - j, i, :] = np.clip(col, 0, 1)
        progress.update()

plt.imsave('images/scene.png', image)
