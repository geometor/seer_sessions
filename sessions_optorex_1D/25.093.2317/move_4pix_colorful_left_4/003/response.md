```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms an input sequence of integers by identifying a 'core block' 
(from the first non-zero element to the last non-zero element, inclusive) 
and shifting this block 4 positions to the left within a new sequence of 
the same length, initialized with zeros. Zeros pad the sequence on the right 
after the shifted block. Elements shifted beyond the beginning of the sequence 
are discarded.
"""

# Helper function to find the indices of the first and last non-zero elements
def find_non_zero_bounds(sequence: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the index of the first and last non-zero element in a list.

    Args:
        sequence: The input list of integers.

    Returns:
        A tuple containing the start and end indices (inclusive) of the 
        non-zero block, or None if no non-zero elements are found.
    """
    first_nz_idx = -1
    last_nz_idx = -1
    for i, val in enumerate(sequence):
        if val != 0:
            if first_nz_idx == -1:
                first_nz_idx = i
            last_nz_idx = i
            
    if first_nz_idx == -1:  # No non-zero elements found
        return None
    else:
        return (first_nz_idx, last_nz_idx)

# Helper function to extract the core block
def extract_core_block(sequence: List[int], start: int, end: int) -> List[int]:
    """
    Extracts a sublist (core block) from the sequence based on start and end indices.

    Args:
        sequence: The input list.
        start: The starting index (inclusive).
        end: The ending index (inclusive).

    Returns:
        The extracted sublist.
    """
    # Ensure indices are valid for slicing
    if start < 0 or end < start or end >= len(sequence):
         # This case shouldn't happen if called after find_non_zero_bounds returns valid indices
         # but added for robustness. If bounds are invalid, return empty list.
         return []
    return sequence[start : end + 1]


def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.
    """
    # Define the fixed shift amount
    shift_amount = 4
    
    # Get the length of the input sequence
    n = len(input_sequence)
    
    # Initialize the output sequence with zeros
    output_sequence = [0] * n 

    # Find the boundaries of the core block (first to last non-zero element)
    bounds = find_non_zero_bounds(input_sequence)

    # If no non-zero elements exist (sequence is all zeros or empty)
    # return the initialized output sequence (all zeros)
    if bounds is None:
        return output_sequence 

    first_nz_idx, last_nz_idx = bounds

    # Extract the core block using the identified boundaries
    core_block = extract_core_block(input_sequence, first_nz_idx, last_nz_idx)
    
    # Calculate the target starting position for the core block in the output sequence
    # by shifting the original start index left by the shift_amount
    output_start_idx = first_nz_idx - shift_amount

    # Place the core block into the output sequence at the calculated position
    # Iterate through the core block elements and their relative indices (i)
    for i, value in enumerate(core_block):
        # Calculate the absolute target index in the output sequence
        target_idx = output_start_idx + i
        
        # Check if the target index is within the valid bounds of the output sequence
        if 0 <= target_idx < n:
            # If valid, place the element from the core block into the output sequence
            output_sequence[target_idx] = value
        # If target_idx is out of bounds ( < 0 or >= n), the element is implicitly discarded

    # Return the constructed output sequence
    return output_sequence
```