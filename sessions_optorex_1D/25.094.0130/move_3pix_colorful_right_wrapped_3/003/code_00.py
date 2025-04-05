"""
Accept a 1-dimensional NumPy array containing 12 integers as input.
Identify three contiguous segments within the input array based on their indices:
    - Segment 1: The first 8 elements (indices 0-7).
    - Segment 2: The single element at index 8.
    - Segment 3: The last 3 elements (indices 9-11).
Construct the output NumPy array by concatenating these segments in a new order:
first Segment 3, then Segment 1, and finally Segment 2.
Return the resulting 12-element NumPy array.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Transforms a 1D NumPy array of 12 integers by rearranging its segments.
    
    Args:
        input_array: A NumPy array of shape (12,) containing integers.

    Returns:
        A NumPy array of shape (12,) with elements rearranged according to the rule:
        [elements 9-11, elements 0-7, element 8].
    """

    # Validate input shape (optional but good practice)
    if input_array.shape != (12,):
        raise ValueError("Input array must have shape (12,)")

    # Extract Segment 1: The first 8 elements (indices 0-7)
    segment_A = input_array[0:8]

    # Extract Segment 2: The single element at index 8
    # Slicing [8:9] keeps it as a 1D array for concatenation
    segment_B = input_array[8:9] 

    # Extract Segment 3: The last 3 elements (indices 9-11)
    segment_C = input_array[9:12]

    # Construct the output array by concatenating segments in the order C, A, B
    output_array = np.concatenate((segment_C, segment_A, segment_B))

    return output_array