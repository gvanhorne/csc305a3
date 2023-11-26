import sys
from typing import List, Tuple
from sphere import Sphere

def write_ppm(filename: str, width: int, height: int, bg_colour: Tuple[float, float, float], near: float, spheres: List[Sphere]):
  """
  Write out a PPM image file.

  Parameters:
  - filename (str): The name of the PPM file to be created.
  - width (int): The width of the image in pixels.
  - height (int): The height of the image in pixels.
  - bg_colour (Tuple[float, float, float]): The color of the background represented as RGB values in the range [0, 1].
  - near (float): Absolute distance from the eye to the image plane along the negative z axis.

  Returns:
  None

  Example usage:
  >>> write_ppm('output.ppm', 3, 2, (1.0, 0.0, 0.0))
  """
  width, height = 2*ncols, 2*nrows

  with open(filename, 'w') as ppm_file:
    ppm_file.write(f"P3\n{ncols} {nrows}\n255\n")

    # Convert background color values to the 0-255 range
    scaled_bg_colour = tuple(int(value * 255) for value in bg_colour)

    for c in range(ncols):
      for r in range(nrows):
        uc = -1*width + width*((2*c) / ncols)
        vr = -1*height + height*((2*r) / nrows)
        camera_coordinates = (uc, vr, -1*near)
        if uc == 0 or vr == 0:
          ppm_file.write(f"{0}, {0}, {0} ")
        else:
          ppm_file.write(f"{scaled_bg_colour[0]}, {scaled_bg_colour[1]}, {scaled_bg_colour[2]} ")
      ppm_file.write("\n")

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
    bg_colour = (scene_dict['BACK'][0], scene_dict['BACK'][1], scene_dict['BACK'][2])
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