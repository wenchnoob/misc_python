import unittest
import adder


class TestAdder(unittest.TestCase):
    def test_addsCorrectly(self):
        a = 10
        b = 5
        res = adder.add(a, b)
        self.assertEqual(res, 15, f"{a} + {b} should equal 15")

    def test_raiseExceptionWithInvalidInput(self):
        a = 'hi'
        b = 3
        with self.assertRaises(ValueError):
            adder.add(a, b)


# unittest.main()
