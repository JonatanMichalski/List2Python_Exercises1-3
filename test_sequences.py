# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 16:09:17 2026

@author: jonas
"""

import unittest

from Exercise_3 import Sequence, DNASequence, RNASequence, ProteinSequence


class TestSequence(unittest.TestCase):
    """Tests for the base Sequence class."""

    def test_base_class_instantiation(self):
        # The base class has no valid characters by default.
        with self.assertRaises(ValueError):
            Sequence("seq1", "ABC")

    def test_identifier_must_be_string(self):
        with self.assertRaises(TypeError):
            DNASequence(123, "ATGC")

    def test_identifier_must_not_be_empty(self):
        with self.assertRaises(ValueError):
            DNASequence("   ", "ATGC")

    def test_data_must_be_string(self):
        with self.assertRaises(TypeError):
            DNASequence("seq1", 123)

    def test_identifier_is_stripped(self):
        sequence = DNASequence("  seq1  ", "ATGC")
        self.assertEqual(sequence.identifier, "seq1")

    def test_sequence_is_converted_to_uppercase(self):
        sequence = DNASequence("seq1", "atgc")
        self.assertEqual(sequence.data, "ATGC")

    def test_len(self):
        sequence = DNASequence("seq1", "ATGC")
        self.assertEqual(len(sequence), 4)

    def test_str_fasta_format(self):
        sequence = DNASequence("seq1", "ATGC")
        self.assertEqual(str(sequence), ">seq1\nATGC")

    def test_empty_sequence_is_allowed(self):
        sequence = DNASequence("empty", "")
        self.assertEqual(len(sequence), 0)
        self.assertEqual(sequence.data, "")

    def test_mutate_replaces_character(self):
        sequence = DNASequence("seq1", "ATGC")
        sequence.mutate(1, "C")
        self.assertEqual(sequence.data, "ACGC")

    def test_mutate_accepts_lowercase_value(self):
        sequence = DNASequence("seq1", "ATGC")
        sequence.mutate(0, "g")
        self.assertEqual(sequence.data, "GTGC")

    def test_mutate_first_and_last_positions(self):
        sequence = DNASequence("seq1", "ATGC")
        sequence.mutate(0, "C")
        sequence.mutate(3, "A")
        self.assertEqual(sequence.data, "CTGA")

    def test_mutate_position_must_be_integer(self):
        sequence = DNASequence("seq1", "ATGC")
        for position in (1.5, "1", True):
            with self.subTest(position=position):
                with self.assertRaises(TypeError):
                    sequence.mutate(position, "A")

    def test_mutate_rejects_out_of_range_positions(self):
        sequence = DNASequence("seq1", "ATGC")
        for position in (-1, 4):
            with self.subTest(position=position):
                with self.assertRaises(ValueError):
                    sequence.mutate(position, "A")

    def test_mutate_value_must_be_string(self):
        sequence = DNASequence("seq1", "ATGC")
        with self.assertRaises(TypeError):
            sequence.mutate(0, 1)

    def test_mutate_rejects_invalid_or_multiple_characters(self):
        sequence = DNASequence("seq1", "ATGC")
        for value in ("N", "AT", ""):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    sequence.mutate(0, value)

    def test_find_motif(self):
        sequence = DNASequence("seq1", "AAGCCGCC")
        self.assertEqual(sequence.find_motif("GCC"), [2, 5])

    def test_find_motif_is_case_insensitive(self):
        sequence = DNASequence("seq1", "AAGCCGCC")
        self.assertEqual(sequence.find_motif("gcc"), [2, 5])
