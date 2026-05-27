"""Small offline bioinformatics helpers for Professor."""

from __future__ import annotations


DNA_COMPLEMENT = str.maketrans("ATGCatgc", "TACGtacg")

CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


def clean_sequence(sequence: str) -> str:
    return "".join(base for base in sequence.upper() if base in "ATGCU")


def gc_content(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if not seq:
        return "Please provide a DNA sequence."
    gc = sum(1 for base in seq if base in "GC")
    percent = (gc / len(seq)) * 100
    return f"GC content is {percent:.2f}% across {len(seq)} bases."


def reverse_complement(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if not seq:
        return "Please provide a DNA sequence."
    return f"Reverse complement: {seq.translate(DNA_COMPLEMENT)[::-1]}"


def transcribe(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if not seq:
        return "Please provide a DNA sequence."
    return f"RNA transcript: {seq.replace('T', 'U')}"


def translate_dna(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if len(seq) < 3:
        return "Please provide a DNA sequence with at least one codon."

    protein = []
    ignored = len(seq) % 3
    for index in range(0, len(seq) - ignored, 3):
        protein.append(CODON_TABLE.get(seq[index : index + 3], "X"))

    note = "" if ignored == 0 else f" Ignored {ignored} trailing base(s)."
    return f"Protein translation: {''.join(protein)}.{note}"


def explain_bioinformatics() -> str:
    return (
        "Bioinformatics uses code and statistics to understand biological data, "
        "such as DNA sequences, RNA expression, proteins, variants, and genomes."
    )
