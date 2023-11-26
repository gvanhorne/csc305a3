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

  def __repr__(self) -> str:
    """
    Return a string representation of the Colour object.

    Returns:
    str: A string containing the representation of the Colour object.
    """
    return f"Colour(r={self.r}, g={self.g}, b={self.b})"
