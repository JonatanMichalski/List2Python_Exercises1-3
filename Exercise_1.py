# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 10:48:17 2026

@author: jonas
"""

class Solution:
    """Represent a chemical or biochemical solution
    
    Attributes:
        name: Name of the dissolved substance.
        concentration: Concentration in mg/mL.
        volume: Volume in mL.
    """
    
    def __init__(self, name: str, concentration: float, volume: float):
        """Initialize a solution with a name, concentration and volume.

        Args:
            name: Non-empty name of the dissolved substance.
            concentration: Positive concentration in mg/mL.
            volume: Positive volume in mL.

        Raises:
            TypeError: If an argument has an invalid type.
            ValueError: If name is is empty or a numeric value is not
                        strictly positive.
        """
        
        if concentration <= 0:
            raise ValueError("Concentration must be greater than 0.")
        if volume <= 0:
            raise ValueError("Volume must be greater than 0.")
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name must not be empty.")

            
        self.name = name.strip()
        self.concentration = float(concentration)
        self.volume = float(volume)
        
    def __str__(self) -> str:
        """Return formatted information about the solution."""
        return(
            f"Solution: {self.name}, "
            f"concentration: {self.concentration:.2f} mg/mL, "
            f"volume: {self.volume:.2f} mL"
        )
    
    def add(self, other: "Solution") -> None:
        """Combine two solutions of the same substance.
        
        The current object is modified in place.
        
        Concentration is calculated using
        conservation of the dissolved substance.

        Args:
            other: Solution to combine with the current solution.

        Raises:
            TypeError: If other is not a Solution.
            ValueError: If the solutions contain different substances.
        """
        
        if not isinstance(other, Solution):
            raise TypeError("Can only combine two Solution objects.")
        
        if self.name != other.name:
            raise ValueError("Solutions must contain the same substance.")
            
        total_volume = self.volume + other.volume 
        # Assumption: neither contraction nor expansion happens 
        
        total_mass = (
            self.concentration * self.volume
            + other.concentration * other.volume
        )
        
        self.concentration = total_mass / total_volume
        self.volume = total_volume
        
    def dilute(self, factor: float) -> None:
        """Reduce concentration by the given dilution factor.
        
        Args:
            factor: Factor greater than 1 by which the volume
                increases.

        Raises:
            ValueError: If factor is not finite or is not greater
                than 1.
        """
        
        if factor <= 1:
            raise ValueError("Dilution factor must be greater than 1.")
            
        self.volume *= factor
        self.concentration /= factor
        
    def __eq__(self, other: object) -> bool:
        """Compare solutions by name and concentration.
        
        Args:
            other: Object to compare with this solution.

        Returns:
            True if both names and concentrations are equal.
            NotImplemented for unsupported object types.
        """
        if not isinstance(other, Solution):
            return NotImplemented
            
        return (
            self.name == other.name
            and self.concentration == other.concentration
        )
