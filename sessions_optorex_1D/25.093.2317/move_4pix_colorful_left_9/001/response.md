```python
import math
import numpy as np # Although not strictly needed for this specific implementation, numpy is often useful for array/grid operations. Let's include it for potential future use or if list slicing becomes complex.

"""
Transforms an input sequence of integers by identifying the segment containing 
all non-zero elements (from the first non-zero to the last non-zero) and 
shifting this segment 4 positions to the left within a sequence of the same 
total length, padding the remaining positions with zeros.
"""

def find_non_zero_indices(sequence):
    """
    Finds the indices of the first and last non-zero elements in a sequence.

    Args:
        sequence: A list of numbers.

    Returns:
        A tuple (first_index, last_index). Returns (None, None) if no 
        non-zero elements are found.
    """
    first_index = None
    last_index = None
    for i, val in enumerate(sequence):
        if val != 0:
            if first_index is None:
                first_index = i
            last_index = i
    return first_index, last_index

def transform(input_sequence):
    """
    Applies the described transformation to the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # Define constants for the transformation
    shift_amount = 4
    sequence_length = len(input_sequence)
    
    # Initialize the output sequence with zeros
    output_sequence = [0] * sequence_length

    # 1. Locate the first and last non-zero elements
    first_nz_idx, last_nz_idx = find_non_zero_indices(input_sequence)

    # 2. Handle the case where no non-zero elements are found
    if first_nz_idx is None:
        # If no non-zeros, the output is already correct (all zeros)
        return output_sequence

    # 3. Extract the active segment
    # The segment includes elements from first_nz_idx up to and including last_nz_idx
    segment = input_sequence[first_nz_idx : last_nz_idx + 1]
    segment_length = len(segment)

    # 4. Calculate the target starting index for the segment in the output
    # Shift the starting position 4 steps to the left
    target_start_idx = first_nz_idx - shift_amount

    # Ensure target start index is not negative (although examples suggest it might be okay if segment goes off left edge, let's stick to placing *within* the bounds for now)
    # Note: Based on examples like train_7, starting at index 0 is valid when input starts at index 4.
    # The logic implicitly handles cases where the shifted segment starts at index 0 or later.

    # 5. Place the extracted segment into the output sequence
    # Calculate the end index for slicing in the output array
    target_end_idx = target_start_idx + segment_length

    # Check bounds to prevent errors if segment shift calculation leads to out-of-bounds indices
    # (This implementation assumes the target indices will fit within the sequence length based on the problem's examples)
    if target_start_idx >= 0 and target_end_idx <= sequence_length:
        output_sequence[target_start_idx:target_end_idx] = segment
    else:
        # Handle cases where the shift might conceptually place part of the segment
        # outside the bounds (e.g., if shift was larger or sequence shorter).
        # For this specific problem/shift=4, this doesn't seem necessary based on examples.
        # A more robust implementation might clip the segment or handle wrap-around if required.
        # Let's proceed assuming valid placement based on observed patterns.
        # If the calculated start is valid, copy the segment.
        if target_start_idx >= 0:
             # Determine how much of the segment fits
            fitting_length = min(segment_length, sequence_length - target_start_idx)
            output_sequence[target_start_idx : target_start_idx + fitting_length] = segment[:fitting_length]
        # If target_start_idx is negative, this indicates an issue or a different rule needed.
        # Given the examples, we assume target_start_idx will always be >= 0.


    # 6. Return the result
    return output_sequence
```