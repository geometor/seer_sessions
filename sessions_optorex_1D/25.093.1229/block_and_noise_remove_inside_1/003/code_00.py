"""
Transforms an input sequence (list or 1D NumPy array) of integers based on the following rule:
1. Identify the segment of the sequence between the first and last non-zero digits (inclusive).
2. If no non-zero digits exist, return the original sequence.
3. Count the frequency of each digit within this segment in the *input* sequence.
4. Determine the digit with the highest frequency (the dominant digit) within that segment.
5. Create a new sequence, initially a copy of the input.
6. Replace all digits within the identified segment boundaries (from the first non-zero index to the last non-zero index, inclusive) in the new sequence with the dominant digit.
7. Digits outside this segment (leading/trailing zeros) remain unchanged.
"""

import numpy as np
from collections import Counter

def find_segment_boundaries(sequence_np):
    """
    Finds the start and end indices of the non-zero segment in a NumPy array.

    Args:
        sequence_np: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) or (None, None) if no non-zero elements.
    """
    # Find indices where the element is not zero
    non_zero_indices = np.where(sequence_np != 0)[0]

    # Check if any non-zero elements were found
    if non_zero_indices.size == 0:
        return None, None  # No non-zero elements found

    # The first non-zero index is the minimum index found
    start_index = non_zero_indices[0]
    # The last non-zero index is the maximum index found
    end_index = non_zero_indices[-1]

    return start_index, end_index

def find_dominant_digit(segment):
    """
    Finds the most frequent digit in a sequence segment.

    Args:
        segment: A list or NumPy array slice representing the segment.

    Returns:
        The most frequent integer digit in the segment, or None if segment is empty.
    """
    # Convert segment (potentially a NumPy slice) to list for Counter
    # This handles potential NumPy scalar types correctly for Counter
    segment_list = list(map(int, segment)) # Ensure elements are standard Python ints

    if not segment_list:
        # This case should ideally not be reached if boundaries are valid
        # and segment is derived from a non-all-zero sequence
        return None

    # Count occurrences of each digit
    counts = Counter(segment_list)

    # Find the digit with the maximum count.
    # most_common(1) returns a list of [ (element, count) ]
    dominant_digit, _ = counts.most_common(1)[0]

    return dominant_digit

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or 1D NumPy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a NumPy array for consistent processing
    sequence_np = np.array(input_sequence)

    # Find the boundaries of the non-zero segment
    start_index, end_index = find_segment_boundaries(sequence_np)

    # Handle the edge case where the sequence is all zeros or empty
    if start_index is None:
        # If no non-zero elements, return the original sequence as a list
        return sequence_np.tolist()

    # Extract the segment from the original input array
    segment = sequence_np[start_index : end_index + 1]

    # Determine the dominant digit in the segment
    dominant_digit = find_dominant_digit(segment)

    # Initialize the output sequence as a copy of the input NumPy array
    # This ensures we work with a mutable copy
    output_sequence_np = sequence_np.copy()

    # Replace the elements within the segment boundaries with the dominant digit
    # Use slicing for efficient modification of the NumPy array
    output_sequence_np[start_index : end_index + 1] = dominant_digit

    # Return the modified sequence as a standard Python list
    return output_sequence_np.tolist()
