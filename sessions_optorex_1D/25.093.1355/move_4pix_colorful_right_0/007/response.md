```python
"""
Transforms an input 1D NumPy array of 12 integers by performing a right shift.
Specifically, it takes the first 8 elements of the input array (indices 0-7)
and places them into a new array of the same size (12 elements), starting
at index 4 (positions 4-11). The first 4 elements (indices 0-3) of the
output array are filled with zeros. The last 4 elements of the input array
(indices 8-11) are effectively discarded.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a right shift transformation to a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of 12 integers.

    Returns:
        A new 1D NumPy array of 12 integers representing the transformed sequence.
    """

    # Define constants based on the observed pattern
    sequence_length = 12 # Expected length of the input/output arrays
    shift_amount = 4     # Number of positions to shift right
    # Calculate the number of elements from the start of the input to copy
    elements_to_copy = sequence_length - shift_amount # 12 - 4 = 8

    # initialize output_grid: Create a new NumPy array of the correct size,
    # filled with zeros, and matching the data type of the input.
    output_grid = np.zeros(sequence_length, dtype=input_grid.dtype)

    # change output elements: Copy the relevant slice from the input to the output.
    # Identify the source slice in the input (first 'elements_to_copy' elements).
    # Indices 0 to 7 (exclusive of 8).
    source_slice = input_grid[0:elements_to_copy]

    # Identify the target slice in the output grid.
    # Starts at 'shift_amount' index and has length 'elements_to_copy'.
    # Indices 4 to 11 (exclusive of 12).
    target_start_index = shift_amount
    target_end_index = shift_amount + elements_to_copy # 4 + 8 = 12

    # Perform the assignment: Place the source slice into the target slice location.
    # Ensure shapes match: source_slice shape is (8,), target slice output_grid[4:12] shape is (8,).
    output_grid[target_start_index:target_end_index] = source_slice

    # The first 'shift_amount' (4) elements of output_grid remain zero from initialization.
    # The last 'shift_amount' (4) elements of input_grid are implicitly ignored.

    return output_grid
```