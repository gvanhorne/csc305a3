import numpy as np

from ray import Ray
from hittable import Hittable, HitRecord
from utils import normalize

class Sphere(Hittable):
  def __init__(self, name, center, scaling, colour, ka, kd, ks, kr, n):
    """
    Initializes a Sphere object with the provided attributes.

    Parameters:
    - center (np.array): NumPy array representing the center (x, y, z) of the sphere.
    - scaling (np.array): NumPy array representing the non-uniform scaling factors (sx, sy, sz) of the sphere.
    - colour (np.array): NumPy array representing the (r, g, b) components of the sphere.
    - ka (float): Coefficient for ambient reflection.
    - kd (float): Coefficient for diffuse reflection.
    - ks (float): Coefficient for specular reflection.
    - kr (float): Coefficient for reflection.
    - n (int): Specular exponent.
    """
    self.name = name
    self.center = np.array(center)
    self.scaling = np.array(scaling)
    self.colour = colour
    self.ka = ka
    self.kd = kd
    self.ks = ks
    self.kr = kr
    self.n = n
    self.transformation_matrix = np.array(
      [
        [scaling[0], 0, 0, center[0]],
        [0, scaling[1], 0, center[1]],
        [0, 0, scaling[2], center[2]],
        [0, 0, 0, 1]
      ]
    )
    self.inverse_transform = np.linalg.inv(self.transformation_matrix)

  @classmethod
  def from_array(cls, input_string):
    """
    Create a Sphere object from the provided input string.

    Parameters:
    - input_string (list): Input string in the format ['name', 'pos x', 'pos y', 'pos z', 'scl x', 'scl y', 'scl z', 'r', 'g', 'b', 'ka', 'kd', 'ks', 'kr', 'n'].

    Returns:
    Sphere: Initialized Sphere object.
    """
    name = input_string[0]
    center = np.array([float(x) for x in input_string[1:4]])
    scaling = np.array([float(x) for x in input_string[4:7]])
    colour = np.array([float(x) for x in input_string[7:10]])
    ka, kd, ks, kr, n = map(float, input_string[10:])
    return cls(name, center, scaling, colour, ka, kd, ks, kr, n)

  def hit(self, r: Ray, ray_tmin: float, ray_tmax: float):
    inverse_transformed_ray = inverse_transform_ray(r, self.inverse_transform)
    intersect = canonical_sphere_intersect(inverse_transformed_ray)
    if not intersect:
      return False
    else:
      t1, t2 = intersect
    intersection_point = r.at(t1)
    inverse_transformed_ray = inverse_transform_ray(r, self.inverse_transform)

    normal = np.matmul(np.append(inverse_transformed_ray.at(t1), 0), np.transpose(self.inverse_transform))
    normal = normal[:-1]
    normal = normalize(normal)
    return HitRecord(self, intersection_point, normal, t1)

def inverse_transform_ray(ray: Ray, transformation_matrix):
    # Inverse transform ray and get S' + c't
    transformed_origin = np.matmul(transformation_matrix, np.append(ray.origin, 1))
    transformed_direction = np.matmul(transformation_matrix, np.append(ray.direction, 0))

    # Drop the homogeneous points
    transformed_origin = transformed_origin[:-1]
    transformed_direction = transformed_direction[:-1]

    inverse_transformed_ray = Ray(transformed_origin, transformed_direction, ray.depth)
    return inverse_transformed_ray

def canonical_sphere_intersect(inverse_transformed_ray: Ray):
    # Find the intersection t_h between inv-ray and canonical object
    return hit_sphere(np.array([0, 0, 0]), 1, inverse_transformed_ray)

def hit_sphere(center: np.array, radius: float, ray: Ray):
  oc = ray.origin - center
  a = np.dot(ray.direction, ray.direction)
  b = 2 * np.dot(oc, ray.direction)
  c = np.dot(oc, oc) - radius**2
  d = b**2 - 4*a*c

  if d < 0:
    return False
  else:
    t1 = (-b - np.sqrt(d)) / (2*a)
    t2 = (-b + np.sqrt(d)) / (2*a)
    return t1, t2
