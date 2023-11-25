class Sphere:
    """
    Represents a sphere in a 3D space.

    Attributes:
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

    def __init__(self, position, scaling, color, ka, kd, ks, kr, n):
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
        self.position = position
        self.scaling = scaling
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kr = kr
        self.n = n