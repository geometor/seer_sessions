```python
"""
Transforms an input sequence (list or array) of 12 integers by shifting 
the first 8 elements 4 positions to the right. The first 4 positions 
of the output sequence are filled with zeros, and elements shifted 
beyond the 12th position are truncated.
"""

import numpy as np

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the right shift transformation to the input sequence.

    Args:
        input_sequence: A NumPy array containing 12 integers.

    Returns:
        A NumPy array containing the transformed 12 integers.
    """
    # Define constants based on observations
    sequence_length = 12
    shift_amount = 4

    # Ensure input has the expected length (optional, but good defensive programming)
    if len(input_sequence) != sequence_length:
        # Or handle the error appropriately based on requirements
        # For now, assume input is always correct length based on examples
        pass 

    # Initialize the output sequence with zeros
    # Using numpy zeros for efficient array creation
    output_sequence = np.zeros(sequence_length, dtype=int)

    # Determine the range of elements to copy from the input
    # Elements from index 0 up to (but not including) sequence_length - shift_amount
    source_end_index = sequence_length - shift_amount 
    elements_to_shift = input_sequence[0:source_end_index]

    # Determine the starting position in the output sequence
    destination_start_index = shift_amount
    
    # Calculate the ending position in the output sequence
    # This is destination_start_index + number of elements shifted
    destination_end_index = destination_start_index + len(elements_to_shift)

    # Copy the relevant elements from the input to the output at the shifted position
    # NumPy slicing allows direct assignment
    output_sequence[destination_start_index:destination_end_index] = elements_to_shift

    # Return the completed output sequence
    return output_sequence

```