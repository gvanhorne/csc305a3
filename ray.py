from vector import Vector

class Ray:
  def __init__(self, origin: Vector, direction: Vector):
    """
    Initialize a Ray object with an origin point and a direction vector.

    Parameters:
    - origin (Vector): A Vector representing the (x, y, z) coordinates of the origin point.
    - direction (Vector): A Vector representing the (I, j, k) components of the direction vector.
    """
    self.origin = origin
    self.direction = direction

  def at(self, t: float) -> Vector:
    """
    Calculate a point along the ray at a given parameter t.

    Parameters:
    - t (float): The parameter value indicating the position along the ray.

    Returns:
    tuple: A Vector representing the (x, y, z) coordinates of the point along the ray at parameter t.
    """
    scaled_direction = Vector(t * self.direction.x(), t * self.direction.y(), t * self.direction.z())
    return Vector(self.origin.x() + scaled_direction.x(), self.origin.y() + scaled_direction.y(), self.origin.z() + scaled_direction.z())