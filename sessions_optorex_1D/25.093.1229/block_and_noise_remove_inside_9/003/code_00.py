"""
Transforms an input list of digits based on the following rules:
1. Identify the contiguous sub-list starting from the index of the first non-zero digit 
   and ending at the index of the last non-zero digit (the "active segment").
2. If no non-zero digits exist in the input list, the output is identical to the input.
3. Determine the digit that appears most frequently within the original active segment 
   (the "dominant digit").
4. Construct the output list by:
   a. Taking the elements from the input list before the active segment.
   b. Appending the dominant digit, repeated for the length of the active segment.
   c. Appending the elements from the input list after the active segment.
The input and output are lists of integers.
"""

from collections import Counter
import numpy as np # numpy might not be strictly necessary but is often available

def _find_active_segment_indices(sequence):
    """
    Finds the start and end indices of the first and last non-zero elements.
    Returns (None, None) if no non-zero elements are found.
    """
    # Convert to list just in case input is a numpy array, simplifying indexing
    sequence_list = list(sequence) 
    non_zero_indices = [i for i, x in enumerate(sequence_list) if x != 0]
    if not non_zero_indices:
        return None, None
    return non_zero_indices[0], non_zero_indices[-1]

def _find_dominant_digit(segment):
    """
    Finds the most frequent digit in a given segment (list or sequence of digits).
    If there's a tie, Counter.most_common(1) returns one of the most frequent.
    """
    if not segment:
        # Should not happen if indices are valid, but handles empty segment case
        return None 
    counts = Counter(segment)
    # most_common(1) returns a list like [(element, count)], so access [0][0]
    dominant_digit, _ = counts.most_common(1)[0]
    return dominant_digit

def transform(input_grid):
    """
    Applies the transformation rule to the input list of integers.
    """
    # Ensure input is treated as a standard Python list for consistency
    input_sequence = list(input_grid) 

    # 1. Identify the active segment indices
    start_index, end_index = _find_active_segment_indices(input_sequence)

    # 2. Handle the case where there are no non-zero digits (or empty list)
    if start_index is None:
        # Return the original list (or an empty list if input was empty)
        return input_sequence 

    # 4. Extract the original active segment using the found indices
    # Slicing is end-exclusive, so add 1 to end_index
    active_segment = input_sequence[start_index : end_index + 1]

    # 5. Find the dominant digit in the original active segment
    dominant_digit = _find_dominant_digit(active_segment)

    # 6. Construct the output list
    #    a. Get the part before the active segment
    prefix = input_sequence[:start_index]
    
    #    b. Create the new middle part with the dominant digit
    segment_length = end_index - start_index + 1
    middle = [dominant_digit] * segment_length
    
    #    c. Get the part after the active segment
    suffix = input_sequence[end_index + 1:]

    # Combine the parts
    output_sequence = prefix + middle + suffix

    # 7. Return the newly constructed list of integers
    # The testing framework might expect a numpy array, but let's return a list
    # as it's the most direct representation of the result. Conversion can happen
    # outside if needed.
    return output_sequence
