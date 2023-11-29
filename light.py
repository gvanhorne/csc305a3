import numpy as np

class Light:
  def __init__(self, name, position, intensity):
    self.name = name
    self.position = position
    self.intensity = intensity

  @classmethod
  def from_array(cls, input_string):
    name = input_string[0]
    position = np.array([float(x) for x in input_string[1:4]])
    intensity = np.array([float(x) for x in input_string[4:7]])
