import unittest
import math
from vector import Vector, dot, cross, unit_vector

class TestVector(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector(1.0, 2.0, 3.0)
        self.v2 = Vector(4.0, 5.0, 6.0)

    def test_vector_creation(self):
        self.assertEqual(self.v1.x(), 1.0)
        self.assertEqual(self.v1.y(), 2.0)
        self.assertEqual(self.v1.z(), 3.0)

    def test_negation(self):
        neg_v1 = -self.v1
        self.assertEqual(neg_v1.x(), -1.0)
        self.assertEqual(neg_v1.y(), -2.0)
        self.assertEqual(neg_v1.z(), -3.0)

    def test_addition(self):
        result = self.v1 + self.v2
        self.assertEqual(result.x(), 5.0)
        self.assertEqual(result.y(), 7.0)
        self.assertEqual(result.z(), 9.0)

    def test_subtraction(self):
        result = self.v2 - self.v1
        self.assertEqual(result.x(), 3.0)
        self.assertEqual(result.y(), 3.0)
        self.assertEqual(result.z(), 3.0)

    def test_multiplication(self):
        result = self.v1 * 2.0
        self.assertEqual(result.x(), 2.0)
        self.assertEqual(result.y(), 4.0)
        self.assertEqual(result.z(), 6.0)

    def test_division(self):
        result = self.v1 / 2.0
        self.assertEqual(result.x(), 0.5)
        self.assertEqual(result.y(), 1.0)
        self.assertEqual(result.z(), 1.5)

    def test_length(self):
        length = self.v1.length()
        self.assertEqual(length, math.sqrt(14.0))

    def test_length_squared(self):
        length_squared = self.v1.length_squared()
        self.assertEqual(length_squared, 14.0)

    def test_dot_product(self):
        result = dot(self.v1, self.v2)
        self.assertEqual(result, 32.0)

    def test_cross_product(self):
        result = cross(self.v1, self.v2)
        self.assertEqual(result.x(), -3.0)
        self.assertEqual(result.y(), 6.0)
        self.assertEqual(result.z(), -3.0)

    def test_unit_vector(self):
        v = Vector(1.0, 2.0, 3.0)
        result = unit_vector(v)
        length = result.length()
        self.assertAlmostEqual(length, 1.0)

if __name__ == '__main__':
    unittest.main()