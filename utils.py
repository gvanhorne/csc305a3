import numpy as np
Point, Vector, Colour = np.array, np.array, np.array # Alias for geometric clarity

def reflect(incident: Vector, normal: Vector):
  """
  Calculate the reflection direction for an incident vector and a normal vector.

  Parameters:
  - incident (Vector): The incident vector.
  - normal (Vector): The normal vector.

  Returns:
  Vector:
      The reflected vector representing the reflection direction.
  """
  incident = normalize(incident)
  normal = normalize(normal)

  reflected = incident - 2 * np.dot(incident, normal) * normal

  return reflected

def normalize(v: Vector):
  """
  Normalize a vector to create a unit vector.

  Parameters:
  - v (Vector): Input vector to be normalized.

  Returns:
  numpy.array:
      A unit vector in the same direction as the input vector `v`.
  """
  norm = np.linalg.norm(v)
  unit_vector = v / norm
  return unit_vector
