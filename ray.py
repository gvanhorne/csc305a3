class Ray:
  def __init__(self, origin, direction):
    self.origin = origin
    self.direction = direction

  def at(self, t):
    """
    Calculate a point along the ray at a given parameter t.
    """
    scaled_direction = tuple(t * d for d in self.direction)
    return tuple(o + sd for o, sd in zip(self.origin, scaled_direction))