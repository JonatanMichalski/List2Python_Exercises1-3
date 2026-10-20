# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:37:09 2026

@author: jonas
"""

import unittest

from Exercise_2 import Patient, Hospital


class TestPatient(unittest.TestCase):
    """Test the Patient class."""

    def setUp(self):
        """Create a sample patient."""
        self.patient = Patient(
            "Bartosz Wilkosz",
            "2004-05-12",
            67,
            "F84",
            True,
        )

    def test_init(self):
        """Test initialization of a patient."""
        self.assertEqual(self.patient.name, "Bartosz Wilkosz")
        self.assertEqual(self.patient.dob, "2004-05-12")
        self.assertEqual(self.patient.id, 67)
        self.assertEqual(self.patient.diagnosis, "F84")
        self.assertTrue(self.patient.admitted)

    def test_init_default_admitted(self):
        """Test that a patient is not admitted by default."""
        patient = Patient("Jan Nowak", "1985-11-03", 102, "J45")
        self.assertFalse(patient.admitted)

    def test_init_empty_name(self):
        """Test that an empty name raises ValueError."""
        with self.assertRaises(ValueError):
            Patient("", "2004-05-12", 67, "F84")

    def test_init_invalid_name_type(self):
        """Test that a non-string name raises TypeError."""
        with self.assertRaises(TypeError):
            Patient(123, "2004-05-12", 67, "F84")

    def test_init_invalid_id_type(self):
        """Test that a non-integer ID raises TypeError."""
        with self.assertRaises(TypeError):
            Patient("Bartosz Wilkosz", "2004-05-12", "67", "F84")

    def test_init_boolean_id(self):
        """Test that a boolean ID raises TypeError."""
        with self.assertRaises(TypeError):
            Patient("Bartosz Wilkosz", "2004-05-12", True, "F84")

    def test_init_empty_dob(self):
        """Test that an empty date of birth raises ValueError."""
        with self.assertRaises(ValueError):
            Patient("Bartosz Wilkosz", "", 67, "F84")

    def test_init_empty_diagnosis(self):
        """Test that an empty diagnosis raises ValueError."""
        with self.assertRaises(ValueError):
            Patient("Bartosz Wilkosz", "2004-05-12", 67, "")

    def test_init_invalid_admitted_type(self):
        """Test that a non-boolean admitted value raises TypeError."""
        with self.assertRaises(TypeError):
            Patient("Bartosz Wilkosz", "2004-05-12", 67, "F84", 1)

    def test_admit(self):
        """Test admitting a patient."""
        self.patient.discharge()
        self.patient.admit()
        self.assertTrue(self.patient.admitted)

    def test_discharge(self):
        """Test discharging a patient."""
        self.patient.discharge()
        self.assertFalse(self.patient.admitted)

    def test_str(self):
        """Test the string representation of a patient."""
        expected = (
            "Patient ID: 67, "
            "Name: Bartosz Wilkosz, "
            "Date of birth: 2004-05-12, "
            "Diagnosis: F84, "
            "Status: Admitted"
        )
        self.assertEqual(str(self.patient), expected)


class TestHospital(unittest.TestCase):
    """Test the Hospital class."""

    def setUp(self):
        """Create a hospital and sample patients."""
        self.hospital = Hospital("Central Hospital")
        self.patient1 = Patient(
            "Bartosz Wilkosz", "2004-05-12", 67, "F84", True
        )
        self.patient2 = Patient(
            "Jan Nowak", "1985-11-03", 102, "J45", False
        )

    def test_init(self):
        """Test initialization of a hospital."""
        self.assertEqual(self.hospital.name, "Central Hospital")
        self.assertEqual(self.hospital.patients, [])

    def test_init_empty_name(self):
        """Test that an empty hospital name raises ValueError."""
        with self.assertRaises(ValueError):
            Hospital("   ")

    def test_init_invalid_name_type(self):
        """Test that a non-string hospital name raises TypeError."""
        with self.assertRaises(TypeError):
            Hospital(123)

    def test_add_patient(self):
        """Test adding a patient to the hospital."""
        self.hospital.add_patient(self.patient1)
        self.assertEqual(len(self.hospital.patients), 1)
        self.assertIs(self.hospital.patients[0], self.patient1)

    def test_add_invalid_object(self):
        """Test that adding a non-Patient object raises TypeError."""
        with self.assertRaises(TypeError):
            self.hospital.add_patient("not a patient")

    def test_add_duplicate_id(self):
        """Test that duplicate patient IDs are rejected."""
        self.hospital.add_patient(self.patient1)

        duplicate = Patient(
            "Peter Smith", "1970-01-01", 67, "E11"
        )

        with self.assertRaises(ValueError):
            self.hospital.add_patient(duplicate)

    def test_discharge_patient(self):
        """Test discharging a patient by ID."""
        self.hospital.add_patient(self.patient1)
        self.hospital.discharge_patient(67)
        self.assertFalse(self.patient1.admitted)

    def test_discharge_patient_not_found(self):
        """Test that an unknown patient ID raises ValueError."""
        with self.assertRaises(ValueError):
            self.hospital.discharge_patient(999)

    def test_discharge_invalid_id_type(self):
        """Test that a non-integer ID raises TypeError."""
        with self.assertRaises(TypeError):
            self.hospital.discharge_patient("67")

    def test_discharge_boolean_id(self):
        """Test that a boolean ID raises TypeError."""
        with self.assertRaises(TypeError):
            self.hospital.discharge_patient(True)

    def test_get_patient_list(self):
        """Test that only admitted patient IDs are returned."""
        self.hospital.add_patient(self.patient1)
        self.hospital.add_patient(self.patient2)

        self.assertEqual(self.hospital.get_patient_list(), [67])

    def test_get_patient_list_after_discharge(self):
        """Test the admitted patient list after a discharge."""
        self.hospital.add_patient(self.patient1)
        self.hospital.add_patient(self.patient2)

        self.hospital.discharge_patient(67)

        self.assertEqual(self.hospital.get_patient_list(), [])

    def test_get_patient_list_after_admission(self):
        """Test the admitted patient list after admitting a patient."""
        self.hospital.add_patient(self.patient2)
        self.patient2.admit()

        self.assertEqual(self.hospital.get_patient_list(), [102])


if __name__ == "__main__":
    unittest.main()