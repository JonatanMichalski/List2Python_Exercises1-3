# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:25:33 2026

@author: jonas
"""

class Patient:
    """Represent a patient in a hospital.
    
    Attributes:
        name: Patient's full name.
        dob: Patient's date of birth.
        patient_id: Unique patient identifier.
        diagnosis: Diagnosis name or ICD-10 code.
        admitted: Whether the patient is currently admitted.       
    """
    
    def __init__(
            self,
            name: str,
            dob: str,
            patient_id: int,
            diagnosis: str,
            admitted: bool = False,
            ) -> None:
        """Initialise a patient with personal and medical information
        
        Args:
            name: Patient's full name.
            dob: Patient's date of birth.
            patient_id: Unique patient identifier.
            diagnosis: Diagnosis name or ICD-10 code.
            admitted: Whether the patient is currently admitted.
            
        Raises:
            TypeError: If an argument has an invalid type.
            ValueError: If a required string is empty.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name must not be empty.")
        
        if not isinstance(patient_id, int):
            raise TypeError("Patient's ID must be an integer number.")

        if not isinstance(dob, str):
            raise TypeError("Date of birth must be a string.")
        if not dob.strip():
            raise ValueError("Date of birth must not be empty.")
            
        if isinstance(patient_id, bool) or not isinstance(
            patient_id, int
        ):
            raise TypeError("Patient ID must be an integer.")

        if not isinstance(diagnosis, str):
            raise TypeError("Diagnosis must be a string.")
        if not diagnosis.strip():
            raise ValueError("Diagnosis must not be empty.")

        if not isinstance(admitted, bool):
            raise TypeError("Admitted must be a boolean.")
            
        self.name = name.strip()
        self.dob = dob.strip()
        self.id = patient_id
        self.diagnosis = diagnosis.strip()
        self.admitted = admitted
        
    def admit(self) -> None:
        """Mark the patient as admitted."""
        self.admitted = True
        
    def discharge(self) -> None:
        """Mark the patient as discharged."""
        self.admitted = False
        
    def __str__(self) -> str:
        """Return a string summarizing the patient's data."""
        status = "Admitted" if self.admitted else "Not admitted"
        
        return(
            f"Patient ID: {self.id}, "
            f"Name: {self.name}, "
            f"Date of birth: {self.dob}, "
            f"Diagnosis: {self.diagnosis}, "
            f"Status: {status}"
        )
    
class Hospital:
    """Represent a hospital and its patients.
    
    Attributes:
        name: Hospital's name.
        patient: List of hospital's patients.     
    """
    
    def __init__(self, name: str):
        """Initialise a hospital with its name and an empty list of patients.
        
        Args:
            name: Hospital's name.

        Raises:
            TypeError: If name is not a string.
            ValueError: If name is empty.
        """
        
        if not isinstance(name, str):
            raise TypeError("Hospital name must be a string.")
        if not name.strip():
            raise ValueError("Hospital name must not be empty.")

        self.name = name.strip()
        self.patients: list[Patient] = []
        
    def add_patient(self, patient: Patient) -> None:
        """Add a patient to the hospital.

        Args:
            patient: Patient object to add.

        Raises:
            TypeError: If patient is not a Patient object.
            ValueError: If a patient with the same ID already exists.
        """
        if not isinstance(patient, Patient):
                raise TypeError("Only Patient objects can be added.")

        for existing_patient in self.patients:
            if existing_patient.id == patient.id:
                raise ValueError("A patient with this ID already exists.")

        self.patients.append(patient)
        
    def discharge_patient(self, patient_id: int) -> None:
        """Discharge a patient using their ID.

        Args:
            patient_id: ID of the patient to discharge.

        Raises:
            TypeError: If patient_id is not an integer.
            ValueError: If no patient with this ID exists.
        """
        if isinstance(patient_id, bool) or not isinstance(
            patient_id, int
        ):
            raise TypeError("Patient ID must be an integer.")
            
        for patient in self.patients:
            if patient.id == patient_id:
                patient.discharge()
                return
        
        raise ValueError("Patient not found.")
        
    def get_patient_list(self) -> list[int]:
        """Return IDs of all currently admitted patients."""
        return [
            patient.id
            for patient in self.patients
            if patient.admitted
        ]
        
            

"""Functionality demonstration."""

def main() -> None:
    """Demonstrate hospital management operations."""
    hospital = Hospital("4. WSK")

    patient1 = Patient(
        "Bartosz Wilkosz",
        "2004-05-12",
        67,
        "F84",
        True,
    )

    patient2 = Patient(
        "Jan Nowak",
        "1985-11-03",
        102,
        "J45",
        False,
    )

    patient3 = Patient(
        "Anna Kowalska",
        "1990-07-21",
        103,
        "E11",
        True,
    )

    # Add patients to the hospital.
    hospital.add_patient(patient1)
    hospital.add_patient(patient2)
    hospital.add_patient(patient3)

    print(f"Hospital: {hospital.name}")

    # Display information about all patients.
    print("\nAll patients:")
    for patient in hospital.patients:
        print(patient)

    # Display IDs of admitted patients.
    print("\nAdmitted patient IDs:")
    print(hospital.get_patient_list())

    # Admit a patient.
    print("\nAdmitting patient 102...")
    patient2.admit()
    print("Admitted patient IDs:", hospital.get_patient_list())

    # Discharge a patient by ID.
    print("\nDischarging patient 67...")
    hospital.discharge_patient(67)
    print("Admitted patient IDs:", hospital.get_patient_list())

    # Display the updated information about the discharged patient.
    print("\nUpdated patient information:")
    print(patient1)


if __name__ == "__main__":
    main()

