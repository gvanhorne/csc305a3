class Colour:
  def __init__(self, r: float, g: float, b: float):
    """
    Initialize a Colour object with red, green, and blue components.

    Parameters:
    - r (float): The red component.
    - g (float): The green component.
    - b (float): The blue component.
    """
    self.r = r
    self.g = g
    self.b = b

  def __add__(self, other: 'Colour') -> 'Colour':
    """
    Override the addition operation for Colour instances.

    Parameters:
    - other (Colour): The Colour to add.

    Returns:
    Colour: A new Colour representing the result of the addition.
    """
    return Colour(self.r + other.r, self.g + other.g, self.b + other.b)

  def __mul__(self, scalar: float) -> 'Colour':
    """
    Multiply the Colour by a scalar.

    Parameters:
    - scalar (float): The scalar factor.

    Returns:
    Colour: A new Colour representing the result of scalar multiplication.
    """
    return Colour(self.r * scalar, self.g * scalar, self.b * scalar)

  def __rmul__(self, scalar: float) -> 'Colour':
    """
    Multiply the Colour by a scalar (commutative).

    Parameters:
    - scalar (float): The scalar factor.

    Returns:
    Colour: A new Colour representing the result of scalar multiplication.
    """
    return self.__mul__(scalar)

  def __repr__(self) -> str:
    """
    Return a string representation of the Colour object.

    Returns:
    str: A string containing the representation of the Colour object.
    """
    return f"Colour(r={self.r}, g={self.g}, b={self.b})"
