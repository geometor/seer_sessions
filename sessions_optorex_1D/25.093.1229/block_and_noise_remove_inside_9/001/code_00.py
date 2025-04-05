"""
Transforms an input sequence of digits based on the following rules:
1. Identify the contiguous sub-sequence starting from the first non-zero digit 
   and ending at the last non-zero digit (the "active segment").
2. If no non-zero digits exist, the output is identical to the input.
3. Determine the digit that appears most frequently within the original active segment 
   (the "dominant digit").
4. Construct the output sequence by:
   a. Taking the digits from the input sequence before the active segment.
   b. Appending the dominant digit, repeated for the length of the active segment.
   c. Appending the digits from the input sequence after the active segment.
"""

from collections import Counter
import numpy as np # Using numpy for potential array operations, though list slicing is sufficient here.

def _find_active_segment_indices(sequence):
    """
    Finds the start and end indices of the first and last non-zero elements.
    Returns (None, None) if no non-zero elements are found.
    """
    non_zero_indices = [i for i, x in enumerate(sequence) if x != 0]
    if not non_zero_indices:
        return None, None
    return non_zero_indices[0], non_zero_indices[-1]

def _find_dominant_digit(segment):
    """
    Finds the most frequent digit in a given segment (list of digits).
    If there's a tie, the one encountered first in Counter's iteration might be chosen,
    or based on the underlying dict order. Examples suggest this isn't critical,
    but using most_common(1) ensures we get the highest frequency.
    """
    if not segment:
        # This case shouldn't happen if called correctly after finding indices,
        # but added for robustness.
        return None 
    counts = Counter(segment)
    # most_common(1) returns a list of tuples [(element, count)]
    dominant_digit, _ = counts.most_common(1)[0]
    return dominant_digit

def transform(input_sequence_str):
    """
    Applies the transformation rule to the input sequence string.
    """
    # Parse the input string into a list of integers
    input_sequence = [int(digit) for digit in input_sequence_str.split()]

    # 1. Identify the active segment indices
    start_index, end_index = _find_active_segment_indices(input_sequence)

    # 2. Handle the case where there are no non-zero digits
    if start_index is None:
        return ' '.join(map(str, input_sequence)) # Return original sequence as string

    # Extract the original active segment
    active_segment = input_sequence[start_index : end_index + 1]

    # 3. Find the dominant digit in the active segment
    dominant_digit = _find_dominant_digit(active_segment)

    # 4. Construct the output sequence
    #    a. Get the part before the active segment
    prefix = input_sequence[:start_index]
    
    #    b. Create the new middle part with the dominant digit
    segment_length = end_index - start_index + 1
    middle = [dominant_digit] * segment_length
    
    #    c. Get the part after the active segment
    suffix = input_sequence[end_index + 1:]

    # Combine the parts
    output_sequence = prefix + middle + suffix

    # Format the output sequence back into a space-separated string
    return ' '.join(map(str, output_sequence))
