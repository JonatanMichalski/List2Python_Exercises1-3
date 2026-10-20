# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:11:56 2026

@author: jonas
"""

"""Unit tests for the Solution class."""

import unittest

from Exercise_1 import Solution


class TestSolution(unittest.TestCase):
    """Test the functionality of the Solution class."""

    def setUp(self):
        """Create sample solutions for the tests."""
        self.solution = Solution("NaCl", 10.0, 100.0)
        self.other_solution = Solution("NaCl", 20.0, 50.0)

    def test_init_valid_values(self):
        """Test initialization with valid values."""
        self.assertEqual(self.solution.name, "NaCl")
        self.assertEqual(self.solution.concentration, 10.0)
        self.assertEqual(self.solution.volume, 100.0)

    def test_init_name_with_whitespace(self):
        """Test that whitespace around the name is removed."""
        solution = Solution("  NaCl  ", 10.0, 100.0)
        self.assertEqual(solution.name, "NaCl")

    def test_init_empty_name(self):
        """Test that an empty name raises ValueError."""
        with self.assertRaises(ValueError):
            Solution("   ", 10.0, 100.0)

    def test_init_non_string_name(self):
        """Test that a non-string name raises TypeError."""
        with self.assertRaises(TypeError):
            Solution(123, 10.0, 100.0)

    def test_init_zero_concentration(self):
        """Test that zero concentration raises ValueError."""
        with self.assertRaises(ValueError):
            Solution("NaCl", 0.0, 100.0)

    def test_init_negative_concentration(self):
        """Test that negative concentration raises ValueError."""
        with self.assertRaises(ValueError):
            Solution("NaCl", -1.0, 100.0)

    def test_init_zero_volume(self):
        """Test that zero volume raises ValueError."""
        with self.assertRaises(ValueError):
            Solution("NaCl", 10.0, 0.0)

    def test_init_negative_volume(self):
        """Test that negative volume raises ValueError."""
        with self.assertRaises(ValueError):
            Solution("NaCl", 10.0, -1.0)

    def test_str(self):
        """Test the string representation of a solution."""
        expected = (
            "Solution: NaCl, concentration: 10.00 mg/mL, "
            "volume: 100.00 mL"
        )
        self.assertEqual(str(self.solution), expected)

    def test_add_solutions(self):
        """Test mixing two solutions of the same substance."""
        self.solution.add(self.other_solution)

        self.assertAlmostEqual(self.solution.concentration, 13.3333333333)
        self.assertEqual(self.solution.volume, 150.0)

    def test_add_different_substances(self):
        """Test that different substances cannot be mixed."""
        other = Solution("KCl", 20.0, 50.0)

        with self.assertRaises(ValueError):
            self.solution.add(other)

    def test_add_invalid_object(self):
        """Test that adding a non-Solution object raises TypeError."""
        with self.assertRaises(TypeError):
            self.solution.add("not a solution")

    def test_dilute(self):
        """Test dilution by a factor of two."""
        self.solution.dilute(2)

        self.assertEqual(self.solution.concentration, 5.0)
        self.assertEqual(self.solution.volume, 200.0)

    def test_dilute_factor_one(self):
        """Test that a dilution factor of one raises ValueError."""
        with self.assertRaises(ValueError):
            self.solution.dilute(1)

    def test_dilute_factor_below_one(self):
        """Test that a factor below one raises ValueError."""
        with self.assertRaises(ValueError):
            self.solution.dilute(0.5)

    def test_equality_same_values(self):
        """Test equality of solutions with matching name and concentration."""
        other = Solution("NaCl", 10.0, 200.0)
        self.assertEqual(self.solution, other)

    def test_equality_different_names(self):
        """Test that solutions with different names are not equal."""
        other = Solution("KCl", 10.0, 100.0)
        self.assertNotEqual(self.solution, other)

    def test_equality_different_concentrations(self):
        """Test that different concentrations make solutions unequal."""
        other = Solution("NaCl", 15.0, 100.0)
        self.assertNotEqual(self.solution, other)

    def test_equality_with_other_type(self):
        """Test comparison with an object of another type."""
        self.assertNotEqual(self.solution, "not a solution")


if __name__ == "__main__":
    unittest.main()