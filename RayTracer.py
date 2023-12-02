import sys
from typing import List
from hittable import HitRecord
from sphere import Sphere
from ray import Ray
from light import Light
import numpy as np
import time
from utils import normalize, reflect
BLACK = np.array([0.0, 0.0, 0.0])
Point, Vector, Colour = np.array, np.array, np.array # Alias for geometric clarity
t_offset = 0.000001 # avoid false intersections due to floating point precision

def intersect_objects(ray: Ray, spheres: List[Sphere]):
  nearest = float('inf')
  closest_hit = False
  for sphere in spheres:
      hit = sphere.hit(ray, float('-inf'), float('inf'))
      if hit and 0 < hit.t < nearest:
        nearest = hit.t
        closest_hit = hit

  if not closest_hit:
    return False

  return closest_hit

def spec_colour(light: Light, hit: HitRecord):
  N = hit.normal
  sphere = hit.obj
  L = normalize(np.subtract(light.position, hit.p + t_offset))
  V = normalize(-hit.p)
  R = reflect(-L, N)

  reflected_dot_view_shiny = np.maximum(np.dot(R, V), 0.0)**sphere.n
  specular = sphere.ks * reflected_dot_view_shiny * light.intensity[:3]
  if (np.dot(L, N) < 0.0):
    return BLACK
  return specular

def shadowray(light: Light, hit: HitRecord, spheres: List[Sphere]):
  L = Ray(hit.p + t_offset, normalize(np.subtract(light.position, hit.p + t_offset)), 1)
  light_dot_normal = np.maximum(0, np.dot(L.direction, hit.normal))
  shadow_source = intersect_objects(L, spheres)
  if shadow_source:
    return BLACK
  return hit.obj.kd * light_dot_normal * light.intensity[:3]
  

def raytrace(r: Ray, spheres: List[Sphere], bg_colour: np.array, lights: List[Light], ambient: Colour):
  if r.depth > r.max_depth:
    return BLACK
  hit = intersect_objects(r, spheres)
  if not hit:
    return bg_colour

  # Ambient
  ambient_colour = ambient * hit.obj.ka

  # Diffuse
  total_diffuse = np.zeros_like(BLACK)
  for light in lights:
    total_diffuse += shadowray(light, hit, spheres)

  # Specular
  total_spec = np.zeros_like(BLACK)
  for light in lights:
    total_spec += spec_colour(light, hit)

  re = Ray(hit.p, reflect(r.direction, normalize(r.direction)), r.depth + 1)
  lighting = ambient_colour + total_diffuse + total_spec
  lighting += hit.obj.kr * raytrace(re, spheres, bg_colour, lights, ambient) # Add the colour returned by reflected ray
  colour = lighting * hit.obj.colour
  return colour

def write_ppm(filename: str, ncols: int, nrows: int, bg_colour: np.array, near: float, spheres: List[Sphere], lights: List[Light], ambient: np.array):
  """
  Write out a PPM image file.

  Parameters:
  - filename (str): The name of the PPM file to be created.
  - width (int): The width of the image in pixels.
  - height (int): The height of the image in pixels.
  - bg_colour (Colour): The colour of the background represented as RGB values in the range [0, 1].
  - near (float): Absolute distance from the eye to the image plane along the negative z axis.

  Returns:
  None

  Example usage:
  >>> write_ppm('output.ppm', 3, 2, (1.0, 0.0, 0.0))
  """
  image_width = ncols
  image_height = nrows

  # Camera
  focal_length = near
  viewport_height = 2.0
  viewport_width = viewport_height * (image_width / image_height)
  camera_center = np.array([0, 0, 0])

  # Calculate the vectors across the horizontal and down the vertical viewport edges.
  viewport_u = np.array([viewport_width, 0, 0])
  viewport_v = np.array([0, -viewport_height, 0])

  # Calculate the location of the upper left pixel.
  pixel_delta_u = viewport_u / image_width
  pixel_delta_v = viewport_v / image_height

  # Calculate the location of the upper left pixel.
  viewport_upper_left = camera_center - np.array([0, 0, focal_length]) - viewport_u/2 - viewport_v/2
  pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

  with open(filename, 'w') as ppm_file:
    ppm_file.write(f"P3\n{ncols} {nrows}\n255\n")

    for j in range(image_height):
      progress_percentage = np.ceil((j + 1) / nrows * 100)
      print(f"\rProgress: {int(progress_percentage)}%", end='', flush=True)
      for i in range(image_width):
        pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
        ray_direction = pixel_center - camera_center
        ray = Ray(camera_center, ray_direction, 1)
        pixel_colour = raytrace(ray, spheres, bg_colour, lights, ambient)

        ppm_file.write(f"{pixel_colour[0]*255}, {pixel_colour[1]*255}, {pixel_colour[2]*255} ")
      ppm_file.write("\n")
    print("\nProcessing complete", flush=True)

def read_image_file(fp: str):
  """
  Reads an input file for an image and creates a dictionary for the pertinent values.

  File Syntax:
    NEAR <n>
    LEFT <l>
    RIGHT <r>
    BOTTOM <b>
    TOP <t>
    RES <x> <y>
    SPHERE <name> <pos x=""> <pos y=""> <pos z=""> <scl x=""> <scl y=""> <scl z="">
            <r> <g> <b> <ka> <kd> <ks> <kr> <n>
            // up to 14 additional sphere specifications
    LIGHT <name> <pos x=""> <pos y=""> <pos z=""> <ir> <ig> <ib>
            // up to 9 additional light specifications
    BACK <r> <g> <b>
    AMBIENT <ir> <ig> <ib>
    OUTPUT <name>

  Args:
      fp (str): The path to the input file.

  Returns:
      dict: A dictionary containing the entries from the input file.
  """
  try:
    scene_dict = {'SPHERES': [], 'LIGHTS': []}

    with open(fp, 'r') as f:
      for line in f:
        line = line.strip().split()

        # Skip empty lines
        if not line:
            continue

        key = line[0]
        if (len(line) == 2):
          value = line[1]
        else:
          value = line[1:]

        if key == 'SPHERE':
          scene_dict['SPHERES'].append(value)
        elif key == 'LIGHT':
          scene_dict['LIGHTS'].append(value)
        else:
          scene_dict[key] = value

  except FileNotFoundError:
      print(f"Error: File '{fp}' not found.")

  return scene_dict

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 RayTracer.py <testcase>.txt")
        sys.exit(1)
    start_time = time.time()
    fp = sys.argv[1]
    scene_dict = read_image_file(fp)
    spheres = []
    lights = []

    ncols, nrows = int(scene_dict['RES'][0]), int(scene_dict['RES'][1])
    near = float(scene_dict['NEAR'])
    filename = scene_dict['OUTPUT']
    ambient_light = np.array([float(x) for x in scene_dict['AMBIENT']])
    bg_colour = np.array([float(x) for x in scene_dict['BACK']])
    for sphere in scene_dict['SPHERES']:
      spheres.append(Sphere.from_array(sphere))
    for light in scene_dict['LIGHTS']:
      lights.append(Light.from_array(light))

    write_ppm(filename, ncols, nrows, bg_colour, near, spheres, lights, ambient_light)
    end_time = time.time()
    elapsed_time = round(end_time - start_time)
    print(f"Elapsed Time: {elapsed_time} seconds", end="", flush=True)
