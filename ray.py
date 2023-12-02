import numpy as np

class Ray:
  max_depth = 3

  def __init__(self, origin: np.array, direction: np.array, depth: int):
    """
    Initialize a Ray object with an origin point and a direction vector.

    Parameters:
    - origin (np.array): A NumPy array representing the (x, y, z) coordinates of the origin point.
    - direction (np.array): A NumPy array representing the (I, j, k) components of the direction vector.
    """
    self.origin = origin
    self.direction = direction
    self.depth = depth

  def at(self, t: float) -> np.array:
    """
    Calculate a point along the ray at a given parameter t.

    Parameters:
    - t (float): The parameter value indicating the position along the ray.

    Returns:
    np.array: A NumPy array representing the (x, y, z) coordinates of the point along the ray at parameter t.
    """
    scaled_direction = t * self.direction
    return self.origin + scaled_direction

  def get_colour(self) -> np.array:
    """
    Get the colour based on the y direction of the ray.

    Returns:
    np.array: A NumPy array representings the (r, g, b) components of the computed colour.
    """
    unit_direction = self.direction / np.linalg.norm(self.direction)
    a = 0.5 * (unit_direction[1] + 1.0)
    return (1.0 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])
