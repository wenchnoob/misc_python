import unittest
import mult


class TestMult(unittest.TestCase):
    def test_multsCorrectly(self):
        a = 10
        b = 5
        res = mult.mult(a, b)
        self.assertEqual(res, 50, f"{a} * {b} should equal 50")

    def test_raiseExceptionWithInvalidInput(self):
        a = 'hi'
        b = 3
        with self.assertRaises(ValueError):
            mult.mult(a, b)