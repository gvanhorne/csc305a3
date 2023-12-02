import sys
from typing import List
from hittable import HitRecord
from sphere import Sphere
from ray import Ray
from light import Light
import numpy as np
import time
from utils import normalize, reflect

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

def ads(pos: np.array, N: np.array, sphere: Sphere, lights: List[Light], ambient: np.array):
  """
  Calculate the Ambient, Diffuse, and Specular (ADS) lighting for a point on a sphere.

  Parameters:
  - pos (numpy.ndarray): The position vector of the point on the sphere.
  - N (numpy.ndarray): The normal vector at the point on the sphere.
  - sphere (Sphere): The sphere object with material properties and color.
  - lights (List[Light]): List of light sources affecting the sphere.
  - ambient (numpy.ndarray): Ambient lighting color.

  Returns:
  numpy.ndarray:
      The color of the point on the sphere based on ADS lighting model.
  """
  ambient_colour = ambient * sphere.ka
  total_diffuse = np.array([0.0, 0.0, 0.0])
  total_specular = np.array([0.0, 0.0, 0.0])

  for light in lights:
    L = normalize(np.subtract(light.position, pos))
    V = normalize(-pos)
    R = reflect(-L, N)

    # Diffuse
    diffuse = np.array([0.0, 0.0, 0.0])
    light_dot_normal = np.maximum(0, np.dot(L, N))
    diffuse = sphere.kd * light_dot_normal * light.intensity[:3]
    total_diffuse = total_diffuse + diffuse

    # Specular
    specular = np.array([0.0, 0.0, 0.0])
    reflected_dot_view_shiny = np.maximum(np.dot(R, V), 0.0)**sphere.n
    specular = sphere.ks * reflected_dot_view_shiny * light.intensity[:3]
    if (np.dot(L, N) < 0.0):
      specular = np.array([0.0, 0.0, 0.0])
    total_specular = total_specular + specular

  lighting = ambient_colour + total_diffuse + total_specular
  colour = lighting * sphere.colour
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
        hit = intersect_objects(ray, spheres)
        if hit:
          pixel_colour = ads(hit.p, hit.normal, hit.obj, lights, ambient)
        else:
          pixel_colour = bg_colour

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
