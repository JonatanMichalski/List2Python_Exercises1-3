# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 14:25:02 2026

@author: jonas
"""

class Sequence:
    """Base class for biological sequences: DNA, RNA and proteins."""
    
    valid_chars = frozenset()
    
    def __init__(self, identifier: str, data: str) -> None:
        """Initialize and validate a biological sequence.

        Args:
            identifier: Sequence identifier.
            data: Sequence data.

        Raises:
            TypeError: If identifier or data is not a string.
            ValueError: If identifier is empty or data contains
                invalid characters.
        """
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be a string.")
        if not identifier.strip():
            raise ValueError("Identifier must not be empty.")
        if not isinstance(data, str):
            raise TypeError("Sequence data must be a string.")

        data = data.upper()

        invalid_chars = set(data) - self.valid_chars
        if invalid_chars:
            raise ValueError(
                f"Invalid sequence characters: {invalid_chars}"
            )

        self.identifier = identifier.strip()
        self.data = data
        
    def __len__(self) -> int:
        """Return the length of the sequence"""
        return len(self.data)
    
    def __str__(self) -> str:
        """Return the sequence in a FASTA-like format."""
        return f">{self.identifier}\n{self.data}"
    
    def mutate(self, position: int, value: str) -> None:
        """Replace a character at the specified zero-based position.
        
        Args:
            position: Zero-based index of the character to replace.
            value: A single valid character.

        Raises:
            TypeError: If position is not an integer or value is not
                a string.
            ValueError: If position is out of range or value is invalid.
        """
        if isinstance(position, bool) or not isinstance(position, int):
            raise TypeError("Position must be an integer number.")
            
        if not isinstance(value, str):
            raise TypeError("Value must be a string.")
            
        value = value.upper()
        
        if position < 0:
            raise ValueError("Position cannot be negative.")
            
        if position >= len(self.data):
            raise ValueError("Position is out of range.")
            
        if len(value) != 1 or value not in self.valid_chars:
            raise ValueError("Value must be a single valid character.")
            
        self.data = (self.data[:position] + value  +self.data[position + 1:])
        
        
    def find_motif(self, motif: str) -> list[int]:
        """Return zero-based positions where a motif occurs.

        Overlapping occurrences are included.

        Args:
            motif: Motif to search for.

        Raises:
            TypeError: If motif is not a string.
            ValueError: If motif is empty or contains invalid characters.
        """
        
        if not isinstance(motif, str):
            raise TypeError("Motif must be a string.")
            
        motif = motif.upper()
        
        if not motif:
            raise ValueError("Motif must not be empty.")
        
        if set(motif) - self.valid_chars:
            raise ValueError("Motif contains invalid characters.")
            
        positions = []
        start = 0
        
        while True:
            position = self.data.find(motif, start)
            
            if position == -1:
                break
            
            positions.append(position)
            start = position + 1
            
        return positions
    
class DNASequence(Sequence):
    """Represent a DNA sequence."""
        
    valid_chars = frozenset("ACGT")
        
    def complement(self) -> "DNASequence":
        """Return the complementary DNA strand in the 5' to 3' direction.

        Uses Watson-Crick base pairing rules: A-T and C-G.

        Returns:
            DNASequence: The complementary DNA sequence.
        """
        pairs = {
            'A': 'T',
            'T': 'A',
            'C': 'G',
            'G': 'C'
        }
        
        complement = ""
        
        for base in self.data:
            complement = pairs[base] + complement
            
        return DNASequence(self.identifier + "_complement", complement)
    
    def transcribe(self) -> "RNASequence":
        """Transcribe a coding DNA strand into RNA.

        The coding-strand convention is used: thymine (T) is replaced
        with uracil (U).
        """
        rna_data = self.data.replace("T", "U")
        return RNASequence(self.identifier, rna_data)
    
class RNASequence(Sequence):
    """Represent an RNA sequence."""
    
    valid_chars = frozenset("AGCU")
    
    def complement(self) -> "RNASequence":
        """Return the complementary RNA sequence.
        Returns:
            RNASequence: The complementary RNA sequence.
        """
        pairs = {
            'A': 'U',
            'U': 'A',
            'C': 'G',
            'G': 'C'
        }
        
        complement = ""
        
        for base in self.data:
            complement = pairs[base] + complement
            
        return RNASequence(self.identifier + "_complement", complement)
    
    def translate(self) -> "ProteinSequence":
        """Translate RNA codons into a protein sequence.

        Translation starts at the first nucleotide, uses complete
        codons, and stops at the first stop codon. An incomplete
        codon at the end is ignored.
        """
        codon_table = {
            "UUU": "F", "UUC": "F",
            "UUA": "L", "UUG": "L",
            "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
            "UAU": "Y", "UAC": "Y",
            "UAA": "STOP", "UAG": "STOP", "UGA": "STOP",
            "UGU": "C", "UGC": "C",
            "UGG": "W",
            "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
            "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
            "CAU": "H", "CAC": "H",
            "CAA": "Q", "CAG": "Q",
            "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
            "AUU": "I", "AUC": "I", "AUA": "I",
            "AUG": "M",
            "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
            "AAU": "N", "AAC": "N",
            "AAA": "K", "AAG": "K",
            "AGU": "S", "AGC": "S",
            "AGA": "R", "AGG": "R",
            "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
            "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
            "GAU": "D", "GAC": "D",
            "GAA": "E", "GAG": "E",
            "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
        }
        
        amino_acids = []
        
        for index in range(0, len(self.data) - 2, 3):
            codon = self.data[index: index + 3]
            amino_acid = codon_table[codon]
            
            if amino_acid == "STOP":
                break
            
            amino_acids.append(amino_acid)
            
        return ProteinSequence(self.identifier, "".join(amino_acids),)
    
class ProteinSequence(Sequence):
    """Represent a protein sequence."""
    
    valid_chars = frozenset("ACDEFGHIKLMNPQRSTVWY")
    
def main() -> None:
    """Demonstrate the biological sequence classes."""
    dna = DNASequence("gene1", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")

    print("DNA sequence:")
    print(dna)
    print("DNA length:", len(dna))

    print("\nDNA complement:")
    print(dna.complement())

    print("\nRNA transcript:")
    rna = dna.transcribe()
    print(rna)

    print("\nProtein translation:")
    protein = rna.translate()
    print(protein)

    print("\nSearching for a DNA motif:")
    print(dna.find_motif("GCC"))

    print("\nMutating DNA:")
    dna.mutate(0, "G")
    print(dna)


if __name__ == "__main__":
    main()
        
            
            
    

                
            