class Sphere:
    """
    Represents a sphere in a 3D space.

    Attributes:
    - name (str): String for the name to be used by the sphere
    - position (tuple): Float tuple representing the position (x, y, z) of the sphere.
    - scaling (tuple): Float tuple representing the non-uniform scaling factors (sx, sy, sz) of the sphere.
    - color (tuple): Three-star float tuple representing the color (r, g, b) of the sphere.
    - ka (float): Coefficient for ambient reflection.
    - kd (float): Coefficient for diffuse reflection.
    - ks (float): Coefficient for specular reflection.
    - kr (float): Coefficient for reflection.
    - n (int): Specular exponent.

    Example:
    >>> sphere = Sphere(position=(0.0, 0.0, -5.0), scaling=(1.0, 1.0, 1.0), color=(1.0, 0.0, 0.0),
    ...                 ka=0.1, kd=0.7, ks=0.2, kr=0.1, n=10)
    """

    def __init__(self, name, position, scaling, color, ka, kd, ks, kr, n):
        """
        Initializes a Sphere object with the provided attributes.

        Parameters:
        - position (tuple): Float tuple representing the position (x, y, z) of the sphere.
        - scaling (tuple): Float tuple representing the non-uniform scaling factors (sx, sy, sz) of the sphere.
        - color (tuple): Float tuple representing the color (r, g, b) of the sphere.
        - ka (float): Coefficient for ambient reflection.
        - kd (float): Coefficient for diffuse reflection.
        - ks (float): Coefficient for specular reflection.
        - kr (float): Coefficient for reflection.
        - n (int): Specular exponent.
        """
        self.name = name
        self.position = position
        self.scaling = scaling
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kr = kr
        self.n = n

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
        position = tuple(map(float, input_string[1:4]))
        scaling = tuple(map(float, input_string[4:7]))
        color = tuple(map(float, input_string[7:10]))
        ka, kd, ks, kr, n = map(float, input_string[10:])
        return cls(name, position, scaling, color, ka, kd, ks, kr, n)

    def __str__(self):
        """
        Returns a string representation of the Sphere object.
        """
        return f"Sphere {self.name}: position={self.position}, scaling={self.scaling}, color={self.color}, ka={self.ka}, kd={self.kd}, ks={self.ks}, kr={self.kr}, n={self.n}"
