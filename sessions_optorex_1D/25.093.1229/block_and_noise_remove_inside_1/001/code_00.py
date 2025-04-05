"""
Transforms an input sequence of digits based on the following rule:
1. Identify the segment of the sequence between the first and last non-zero digits (inclusive).
2. If no non-zero digits exist, return the original sequence.
3. Count the frequency of each digit within this segment.
4. Determine the digit with the highest frequency (the dominant digit) within the segment.
5. Create a new sequence by replacing all digits within the identified segment (from the first non-zero to the last non-zero index) with the dominant digit.
6. Digits outside this segment (leading/trailing zeros) remain unchanged.
"""

from collections import Counter
import numpy as np

def find_segment_boundaries(sequence):
    """Finds the start and end indices of the non-zero segment."""
    non_zero_indices = [i for i, x in enumerate(sequence) if x != 0]
    if not non_zero_indices:
        return None, None  # No non-zero elements found
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    return start_index, end_index

def find_dominant_digit(segment):
    """Finds the most frequent digit in a segment."""
    if not segment:
        return None # Should not happen if boundaries are valid
    counts = Counter(segment)
    # Find the element with the maximum count. If there's a tie, Counter typically returns one of them.
    # The specific tie-breaking rule might not matter based on examples, but most_common(1) handles it.
    dominant_digit, _ = counts.most_common(1)[0]
    return dominant_digit

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # Convert input string to list of ints if necessary (assuming it might be string)
    # For this problem, the input format seems to be space-separated string
    # Let's assume the input is already a list/array of integers for consistency
    # with grid-based problems, though here it's 1D.
    if isinstance(input_sequence, str):
         sequence = [int(x) for x in input_sequence.split()]
    else: # Assume it's already list-like
         sequence = list(input_sequence)


    # Find the boundaries of the non-zero segment
    start_index, end_index = find_segment_boundaries(sequence)

    # Handle the edge case where the sequence is all zeros or empty
    if start_index is None:
        return sequence # Return original sequence

    # Extract the segment
    segment = sequence[start_index : end_index + 1]

    # Determine the dominant digit in the segment
    dominant_digit = find_dominant_digit(segment)

    # Initialize the output sequence as a copy of the input
    output_sequence = list(sequence) # Make a mutable copy

    # Replace the elements within the segment boundaries with the dominant digit
    for i in range(start_index, end_index + 1):
        output_sequence[i] = dominant_digit

    return output_sequence
