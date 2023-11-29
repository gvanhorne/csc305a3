import sys
from typing import List
from sphere import Sphere
from ray import Ray
from light import Light
import numpy as np
import time

# vec4 ads(vec3 pos, vec3 lpos, vec3 N) {
#   vec3 L = normalize(lpos - pos) ;
#   vec3 V = normalize(-pos) ;
#   vec3 R = reflect(-L, N) ;

#   // Compute terms in the illumination equation
#   float lightDotNormal = max( dot(L, N), 0.0 );
#   vec4 diffuse = vec4(0.0, 0.0, 0.0, 1.0);
#   diffuse = diffuseProduct * lightDotNormal;
#   float reflectedDotViewShiny = pow( max(dot(R, V), 0.0), shininess );
#   vec4 specular = vec4(0.0, 0.0, 0.0, 1.0);

#   specular = specularProduct * reflectedDotViewShiny;
#   if( dot(L, N) < 0.0 ) {
#   specular = vec4(0.0, 0.0, 0.0, 1.0); }
#   vec4 color = ambientProduct + diffuse + specular; color.a = 1.0 ;
#   return color ;
# }

def ads_lighting(pos: np.array, lpos: np.array, N: np.array, ambient_color: np.array, diffuse_color: np.array, specular_color: np.array, shininess: float):
    """
    Calculate ambient, diffuse, and specular lighting using the Phong reflection model.

    Parameters:
    - pos: Position of the point in 3D space.
    - lpos: Position of the light source in 3D space.
    - N: Normal vector at the point.
    - ambient_color: Color of the ambient light.
    - diffuse_color: Color of the diffuse light.
    - specular_color: Color of the specular light.
    - shininess: Shininess coefficient for specular reflection.

    Returns:
    - Final color at the point.
    """
    # Calculate ambient component
    ambient = ambient_color

    # Calculate diffuse component
    L = np.linalg.norm(lpos - pos)
    diffuse = max(np.dot(N, L), 0) * diffuse_color

    # Calculate specular component
    R = 2 * np.dot(N, L) * N - L
    V = np.linalg.norm(np.array([0, 0, 1]) - pos)  # Assuming view direction is (0, 0, 1)
    specular = max(np.dot(R, V), 0) ** shininess * specular_color

    # Sum up all components
    result_color = ambient + diffuse + specular

    # Ensure the color values are in the valid range [0, 1]
    result_color = np.clip(result_color, 0, 1)

    return result_color


def hit_sphere(center: np.array, radius: float, ray: Ray):
  oc = ray.origin - center
  a = np.linalg.norm(ray.direction)**2
  half_b = np.dot(oc, ray.direction)
  c = np.linalg.norm(oc)**2 - radius*radius
  discriminant = half_b*half_b - a*c

  if discriminant < 0:
    return -1
  else:
    return (-half_b - np.sqrt(discriminant)) / a

def write_ppm(filename: str, ncols: int, nrows: int, bg_colour: np.array, near: float, spheres: List[Sphere], lights: List[Light]):
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

  sphere = spheres[0]

  with open(filename, 'w') as ppm_file:
    ppm_file.write(f"P3\n{ncols} {nrows}\n255\n")

    for j in range(image_height):
      progress_percentage = np.ceil((j + 1) / nrows * 100)
      print(f"\rProgress: {int(progress_percentage)}%", end='', flush=True)
      for i in range(image_width):
        pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
        ray_direction = pixel_center - camera_center
        ray = Ray(camera_center, ray_direction)
        pixel_colour = bg_colour
        closest_intersect = float('inf')
        for sphere in spheres:
          inverse_transformed_ray = Ray(np.dot(sphere.inverse_transform, np.append(ray.origin, 1)),
                                        np.dot(sphere.inverse_transform, np.append(ray.direction, 0)))
          # Drop the homogeneous points
          inverse_transformed_ray.origin = inverse_transformed_ray.origin[:-1]
          inverse_transformed_ray.direction = inverse_transformed_ray.direction[:-1]

          intersection = hit_sphere(np.array([0, 0, 0]), 1, inverse_transformed_ray)
          if intersection > 0 and intersection < closest_intersect:
            closest_intersect = intersection
            # surface_normal = inverse_transformed_ray.direction / np.linalg.norm(inverse_transformed_ray.at(intersection) - np.array([0, 0, -1]))
            # pixel_colour = 0.5*np.array([surface_normal[0]+1, surface_normal[1]+1, surface_normal[2]+1])
            # pixel_colour = ads_lighting(inverse_transformed_ray.at(intersection), )
            pixel_colour = sphere.colour

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
    bg_colour = np.array(scene_dict['BACK'])
    for sphere in scene_dict['SPHERES']:
      spheres.append(Sphere.from_array(sphere))
    for light in scene_dict['LIGHTS']:
      lights.append(Light.from_array(light))

    write_ppm(filename, ncols, nrows, bg_colour, near, spheres, lights)
    end_time = time.time()
    elapsed_time = round(end_time - start_time)
    print(f"Elapsed Time: {elapsed_time} seconds", end="")
