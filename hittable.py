class HitRecord:
  def __init__(self, obj, p, normal, t):
    self.obj = obj
    self.p = p
    self.normal = normal
    self.t = t

class Hittable:
  def hit(self, ray):
    raise NotImplementedError("Subclasses must implement the 'hit' method")