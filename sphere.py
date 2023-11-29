import numpy as np

class Sphere:
    """
    Represents a sphere in a 3D space.

    Attributes:
    - name (str): String for the name to be used by the sphere
    - position (np.array): NumPy array representing the position (x, y, z) of the sphere.
    - scaling (np.array): NumPy array representing the non-uniform scaling factors (sx, sy, sz) of the sphere.
    - colour (np.array): NumPy array representing the (r, g, b) components of the sphere.
    - ka (float): Coefficient for ambient reflection.
    - kd (float): Coefficient for diffuse reflection.
    - ks (float): Coefficient for specular reflection.
    - kr (float): Coefficient for reflection.
    - n (int): Specular exponent.
    - transformation_matrix (np.array): 4x4 transformation matrix for transformation.

    Example:
    >>> sphere = Sphere(name='example', position=np.array([0.0, 0.0, -5.0]), scaling=np.array([1.0, 1.0, 1.0]), colour=np.array([1.0, 0.0, 0.0]),
    ...                 ka=0.1, kd=0.7, ks=0.2, kr=0.1, n=10)
    """

    def __init__(self, name, position, scaling, colour, ka, kd, ks, kr, n):
        """
        Initializes a Sphere object with the provided attributes.

        Parameters:
        - position (np.array): NumPy array representing the position (x, y, z) of the sphere.
        - scaling (np.array): NumPy array representing the non-uniform scaling factors (sx, sy, sz) of the sphere.
        - colour (np.array): NumPy array representing the (r, g, b) components of the sphere.
        - ka (float): Coefficient for ambient reflection.
        - kd (float): Coefficient for diffuse reflection.
        - ks (float): Coefficient for specular reflection.
        - kr (float): Coefficient for reflection.
        - n (int): Specular exponent.
        """
        self.name = name
        self.position = np.array(position)
        self.scaling = np.array(scaling)
        self.colour = colour
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kr = kr
        self.n = n
        self.transformation_matrix = np.array(
          [
            [scaling[0], 0, 0, position[0]],
            [0, scaling[1], 0, position[1]],
            [0, 0, scaling[2], position[2]],
            [0, 0, 0, 1]
          ]
        )
        self.inverse_transform = np.linalg.inv(self.transformation_matrix)

    @classmethod
    def from_array(cls, input_string):
        """
        Create a Sphere object from the provided input string.

        Parameters:
        - input_string (list): Input string in the format ['name', 'pos x', 'pos y', 'pos z', 'scl x', 'scl y', 'scl z', 'r', 'g', 'b', 'ka', 'kd', 'ks', 'kr', 'n'].

        Returns:
        Sphere: Initialized Sphere object.
        """
        name = input_string[0]
        position = np.array([float(x) for x in input_string[1:4]])
        scaling = np.array([float(x) for x in input_string[4:7]])
        colour = np.array([float(x) for x in input_string[7:10]])
        ka, kd, ks, kr, n = map(float, input_string[10:])
        return cls(name, position, scaling, colour, ka, kd, ks, kr, n)

    def get_normal(self, surface_point):
      return np.subtract(surface_point, self.position)

    def __str__(self):
        """
        Returns a string representation of the Sphere object.
        """
        return f"Sphere {self.name}: position={repr(self.position)}, scaling={repr(self.scaling)}, colour={repr(self.colour)}, ka={self.ka}, kd={self.kd}, ks={self.ks}, kr={self.kr}, n={self.n}"
