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

  def get_norm(self) -> float:
    """
    Get the norm (magnitude) of the ray's direction vector.

    Returns:
    float: The norm of the direction vector.
    """
    return np.linalg.norm(self.direction)
