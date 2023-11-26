from typing import Tuple
import math

class Ray:
  def __init__(self, origin: Tuple[float, float, float], direction: Tuple[float, float, float]):
    """
    Initialize a Ray object with an origin point and a direction vector.

    Parameters:
    - origin (tuple): A tuple representing the (x, y, z) coordinates of the origin point.
    - direction (tuple): A tuple representing the (I, j, k) components of the direction vector.
    """
    self.origin = tuple(origin)
    self.direction = tuple(direction)

  def at(self, t: float) -> Tuple[float, float, float]:
    """
    Calculate a point along the ray at a given parameter t.

    Parameters:
    - t (float): The parameter value indicating the position along the ray.

    Returns:
    tuple: A tuple representing the (x, y, z) coordinates of the point along the ray at parameter t.
    """
    scaled_direction = tuple(t * d for d in self.direction)
    return tuple(o + sd for o, sd in zip(self.origin, scaled_direction))

  def normalized_direction(self) -> Tuple[float, float, float]:
    """
    Return the normalized direction vector.

    Returns:
    Tuple[float, float, float]: The normalized direction vector.
    """
    length = math.sqrt(sum(component**2 for component in self.direction))
    normalized_vector = tuple(component / length for component in self.direction)
    return normalized_vector