import math

class Vector:
  def __init__(self, e0: float, e1: float, e2: float):
    """
    Initialize a Vector object with three components.

    Parameters:
    - e0 (float): The first component.
    - e1 (float): The second component.
    - e2 (float): The third component.
    """
    self.e = [e0, e1, e2]

  def x(self) -> float:
    """Return the x component."""
    return self.e[0]

  def y(self) -> float:
    """Return the y component."""
    return self.e[1]

  def z(self) -> float:
    """Return the z component."""
    return self.e[2]

  def __neg__(self) -> 'Vector':
    """Return the negation of the vector."""
    return Vector(-self.e[0], -self.e[1], -self.e[2])

  def __getitem__(self, i: int) -> float:
    """Get the i-th component."""
    return self.e[i]

  def __setitem__(self, i: int, value: float):
    """Set the i-th component to the given value."""
    self.e[i] = value

  def __iadd__(self, v: 'Vector') -> 'Vector':
    """
    In-place addition with another Vector.

    Parameters:
    - v ('Vector'): Another Vector object.

    Returns:
    'Vector': The resulting Vector after addition.
    """
    self.e[0] += v.e[0]
    self.e[1] += v.e[1]
    self.e[2] += v.e[2]
    return self

  def __imul__(self, t: float) -> 'Vector':
    """
    In-place multiplication by a scalar.

    Parameters:
    - t (float): The scalar factor.

    Returns:
    'Vector': The resulting Vector after multiplication.
    """
    self.e[0] *= t
    self.e[1] *= t
    self.e[2] *= t
    return self

  def __itruediv__(self, t: float) -> 'Vector':
    """
    In-place division by a scalar.

    Parameters:
    - t (float): The scalar divisor.

    Returns:
    'Vector': The resulting Vector after division.
    """
    return self.__imul__(1/t)

  def length(self) -> float:
    """Return the length of the vector."""
    return math.sqrt(self.length_squared())

  def length_squared(self) -> float:
    """Return the squared length of the vector."""
    return self.e[0]**2 + self.e[1]**2 + self.e[2]**2

def dot(u: Vector, v: Vector) -> float:
    """
    Calculate the dot product of two Vector vectors.

    Parameters:
    - u (Vector): The first vector.
    - v (Vector): The second vector.

    Returns:
    float: The dot product of the two vectors.
    """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]

def cross(u: Vector, v: Vector) -> Vector:
    """
    Calculate the cross product of two Vector vectors.

    Parameters:
    - u (Vector): The first vector.
    - v (Vector): The second vector.

    Returns:
    Vector: The cross product of the two vectors.
    """
    return Vector(u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])

def unit_vector(v: Vector) -> Vector:
    """
    Return the unit vector of a Vector vector.

    Parameters:
    - v (Vector): The input vector.

    Returns:
    Vector: The unit vector of the input vector.
    """
    return v / v.length()
