import sys
from typing import List
from sphere import Sphere
from ray import Ray
from vector import Vector
from colour import Colour
Point = Vector

def write_ppm(filename: str, ncols: int, nrows: int, bg_colour: Colour, near: float, spheres: List[Sphere]):
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
  camera_center = Point(0, 0, 0)

  # Calculate the vectors across the horizontal and down the vertical viewport edges.
  viewport_u = Vector(viewport_width, 0, 0)
  viewport_v = Vector(0, -viewport_height, 0)

  # Calculate the location of the upper left pixel.
  pixel_delta_u = viewport_u / image_width
  pixel_delta_v = viewport_v / image_height

  # Calculate the location of the upper left pixel.
  viewport_upper_left = camera_center - Point(0, 0, focal_length) - viewport_u/2 - viewport_v/2
  pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)
 
  with open(filename, 'w') as ppm_file:
    ppm_file.write(f"P3\n{ncols} {nrows}\n255\n")

    for j in range(image_height):
      print(f"\rProgress: {int((j + 1) / nrows * 100)}%", end='', flush=True)
      for i in range(image_width):
        pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
        ray_direction = pixel_center - camera_center
        ray = Ray(camera_center, ray_direction)
        pixel_colour = ray.get_colour()
        ppm_file.write(f"{pixel_colour.r*255}, {pixel_colour.g*255}, {pixel_colour.b*255} ")
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
    fp = sys.argv[1]
    scene_dict = read_image_file(fp)
    spheres = []

    ncols, nrows = int(scene_dict['RES'][0]), int(scene_dict['RES'][1])
    near = float(scene_dict['NEAR'])
    filename = scene_dict['OUTPUT']
    bg_colour = Colour(*scene_dict['BACK'])
    for sphere in scene_dict['SPHERES']:
      spheres.append(Sphere.from_array(sphere))

    write_ppm(filename, ncols, nrows, bg_colour, near, spheres)
    # for c in range(width):
    #   for r in range(height):
    #     print(f"Pixel Coordinate: ({c}, {r})")

    # Function Main
      # for each pixel (c,r) on screen
      #  determine ray rc,r from eye through pixel
      #  ray.setDepth(1)
      #  color(c,r) = raytrace(rc,r )
      # end for
    # end
    # function raytrace(r)
      # if (ray.depth() > MAX_DEPTH) return black
      # P = closest intersection of ray with all objects
      # if( no intersection ) return backgroundColor
      # clocal = Sum(shadowRays(P,Lighti))
      # cre = raytrace(rre)
      # return (clocal+kre*cre)
    # end