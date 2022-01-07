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


def normalize(vector):
    return vector / np.linalg.norm(vector)


def reflect(vector, normal):
    return vector - 2 * np.dot(vector, normal) * normal


def intersect_plane(O, D, P, N):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # plane (P, N), or +inf if there is no intersection.
    # O and P are 3D points, D and N (normal) are normalized vectors.

    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - O, N) / denom
    if d < 0:
        return np.inf
    return d


def intersect_sphere(O, D, S, R):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # sphere (S, R), or +inf if there is no intersection.
    # O and S are 3D points, D (direction) is a normalized vector, R is a scalar.

    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
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


def intersect_triangle(O, R, v0, v1, v2):
    # Compute plane's normal
    v0v1 = v1 - v0
    v0v2 = v2 - v0
    N = normalize(np.cross(v0v1, v0v2))
    D = np.dot(N, v0)

    # Dot product of the triangle's normal and the ray's direction.
    product = np.dot(N, R)

    # The dot product of two perpendicular vectors is 0,
    # so if the ray and the plane are parallel they wont intersect.
    if product == 0:
        return np.inf

    # Distance from the ray origin O to P.
    t = - (np.dot(N, O) + D) / product

    # Check if the triangle is behind the ray.
    if t < 0:
        return np.inf

    # Compute intersection point with ray parametric equation.
    P = O + t * R

    edge0 = v1 - v0
    edge1 = v2 - v1
    edge2 = v0 - v2

    vp0 = P - v0
    vp1 = P - v1
    vp2 = P - v2

    C0 = np.cross(edge0, vp0)
    C1 = np.cross(edge1, vp1)
    C2 = np.cross(edge2, vp2)

    # Check if P is inside the triangle
    if np.dot(N, C0) < 0 or np.dot(N, C1) < 0 or np.dot(N, C2) < 0:
        return np.inf

    return t


def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])
    elif obj['type'] == 'triangle':
        return intersect_triangle(O, D, obj['v0'], obj['v1'], obj['v2'])


def get_normal(obj, M):
    # Find normal.
    if obj['type'] == 'sphere':
        return normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        return obj['normal']
    elif obj['type'] == 'triangle':
        v0v1 = obj['v1'] - obj['v0']
        v0v2 = obj['v2'] - obj['v0']

        return normalize(np.cross(v0v1, v0v2))


def get_color(obj, M):
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    return color


def trace_ray(rayO, rayD):
    # Find first point of intersection with the scene.
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = intersect(rayO, rayD, obj)
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
    N = get_normal(obj, M)
    color = get_color(obj, M)
    toO = normalize(O - M)

    # Start computing the color.
    col_ray = ambient
    has_light = False
    for L, color_light in lights:
        toL = normalize(L - M)

        # Shadow: find if the point is shadowed or not.
        l = [intersect(M + N * 0.0001, toL, obj_sh)
             for k, obj_sh in enumerate(scene) if k != obj_idx]
        if not (l and min(l) < np.inf):
            has_light = True

        # Lambert shading (diffuse).
        col_ray += obj.get('diffuse_c', diffuse_c) * \
            max(np.dot(N, toL), 0) * color

        # Blinn-Phong shading (specular).
        col_ray += obj.get('specular_c', specular_c) * max(np.dot(N,
                                                                  normalize(toL + toO)), 0) ** specular_k * color_light
    if not has_light:
        return

    return obj, M, N, col_ray


def add_plane(position, normal):
    return {
        'type': 'plane',
        'position': np.array(position),
        'normal': np.array(normal),
        'color': lambda M: (np.ones(3) if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else np.zeros(3)),
        'diffuse_c': 0.75,
        'specular_c': 0.5,
        'reflection': 0.25
    }


def add_sphere(position, radius, color):
    return {
        'type': 'sphere',
        'position': np.array(position),
        'radius': np.array(radius),
        'color': np.array(color),
        'reflection': 0.5
    }


def add_triangle(position0, position1, position2, color):
    # Define the 3 vertices of the triangle in counter-clockwise order
    return {
        'type': 'triangle',
        'v0': np.array(position0),
        'v1': np.array(position1),
        'v2': np.array(position2),
        'color': np.array(color)
    }


# Image dimensions
width = 400
height = 300

# Default light and material parameters.
ambient = 0.05
diffuse_c = 1.0
specular_c = 1.0
specular_k = 50

# Maximum number of light reflections.
depth_max = 5

# List of objects.
scene = [
    add_plane([0.0, -0.5, 0.0], [0.0, 1.0, 0.0]),
    add_sphere([0.75, 0.1, 1.0], 0.6, [0.0, 0.0, 1.0]),  # Blue
    add_sphere([-0.75, 0.1, 2.25], 0.6, [0.5, 0.223, 0.5]),  # Purple
    add_sphere([-2.75, 0.1, 3.5], 0.6, [1.0, 0.572, 0.184]),  # Orange
    add_triangle([-0.5, -0.5, -0.5], [-1.0, -0.5, -0.5], [-1.0, 0.0, -0.5],
                 [0.0, 1.0, 0.0]),
    add_triangle([0.5, -0.5, 0.5], [0.5, 0.0, 1.0], [0.5, -0.5, 1.0],
                 [1.0, 0.0, 0.0]),
]

# List of light positions and colors.
lights = [
    (np.array([5.0, 5.0, -10.0]), np.array([1.0, 1.0, 1.0])),  # White
    (np.array([-10.0, 5.0, 5.0]), np.array([1.0, 0.0, 1.0])),  # Red
]

# Camera view.
O = np.array([0.0, 0.35, -1.0])  # Camera.
Q = np.array([0.0, 0.0, 0.0])  # Camera pointing to.

# Screen coordinates (left, top, right, bottom): x0, y0, x1, y1.
ratio = width / height
S = (-1.0, -1.0 / ratio + 0.25, 1.0, 1.0 / ratio + 0.25)

# Loop through all pixels.
image = np.zeros((height, width, 3))
with tqdm(total=width * height) as progress:
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
                rayO, rayD = M + N * 0.0001, normalize(reflect(rayD, N))

                col += reflection * col_ray
                reflection *= obj.get('reflection', 1.0)

            image[height - 1 - j, i, :] = np.clip(col, 0, 1)
            progress.update()

plt.imsave('images/scene.png', image)
