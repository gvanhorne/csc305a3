import numpy as np

def reflect(incident: np.array, normal: np.array):
  """
  Calculate the reflection direction for an incident vector and a normal vector.

  Parameters:
  - incident (numpy.array): The incident vector.
  - normal (numpy.array): The normal vector.

  Returns:
  numpy.array:
      The reflected vector representing the reflection direction.
  """
  incident = normalize(incident)
  normal = normalize(normal)

  reflected = incident - 2 * np.dot(incident, normal) * normal

  return reflected

def normalize(v: np.array):
  """
  Normalize a vector to create a unit vector.

  Parameters:
  - v (numpy.array): Input vector to be normalized.

  Returns:
  numpy.array:
      A unit vector in the same direction as the input vector `v`.
  """
  norm = np.linalg.norm(v)
  unit_vector = v / norm
  return unit_vector