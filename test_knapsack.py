
import unittest

from algorithms.knapsack import optimize_appliances


class TestPowerWiseKnapsack(unittest.TestCase):

    def setUp(self):
        self.appliances = [
            {"name": "Fan", "power_w": 75, "priority": 8},
            {"name": "Refrigerator", "power_w": 200, "priority": 10},
            {"name": "Television", "power_w": 120, "priority": 5},
            {"name": "Washing Machine", "power_w": 500, "priority": 7},
            {"name": "Air Conditioner", "power_w": 1500, "priority": 9}
        ]

    def test_normal_case(self):
        result = optimize_appliances(self.appliances, 2000)

        self.assertEqual(result["total_priority"], 32)
        self.assertEqual(result["total_power"], 1895)
        self.assertLessEqual(result["total_power"], 2000)

    def test_zero_capacity(self):
        result = optimize_appliances(self.appliances, 0)

        self.assertEqual(result["total_priority"], 0)
        self.assertEqual(result["total_power"], 0)
        self.assertEqual(result["selected"], [])

    def test_exact_capacity(self):
        appliances = [
            {"name": "Heater", "power_w": 500, "priority": 8}
        ]

        result = optimize_appliances(appliances, 500)

        self.assertEqual(result["total_power"], 500)
        self.assertEqual(result["total_priority"], 8)

    def test_insufficient_capacity(self):
        appliances = [
            {"name": "Heater", "power_w": 500, "priority": 8}
        ]

        result = optimize_appliances(appliances, 200)

        self.assertEqual(result["selected"], [])

    def test_empty_appliances(self):
        result = optimize_appliances([], 1000)

        self.assertEqual(result["selected"], [])
        self.assertEqual(result["total_priority"], 0)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            optimize_appliances(self.appliances, -100)

    def test_invalid_power(self):
        appliances = [
            {"name": "Fan", "power_w": 0, "priority": 8}
        ]

        with self.assertRaises(ValueError):
            optimize_appliances(appliances, 1000)

    def test_invalid_priority(self):
        appliances = [
            {"name": "Fan", "power_w": 75, "priority": -2}
        ]

        with self.assertRaises(ValueError):
            optimize_appliances(appliances, 1000)


if __name__ == "__main__":
    unittest.main()
