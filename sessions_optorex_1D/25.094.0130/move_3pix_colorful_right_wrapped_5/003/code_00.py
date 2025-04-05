"""
Transforms a 1D numerical array of 12 elements by applying a circular right 
shift of 3 positions. The last 3 elements of the input array become the 
first 3 elements of the output array, and the first 9 elements of the input 
array follow them.
"""

import numpy as np

# Helper function to extract the last n elements
def extract_last_n(arr: np.ndarray, n: int) -> np.ndarray:
    """Extracts the last n elements from a numpy array."""
    return arr[-n:]

# Helper function to extract the first m elements
def extract_first_m(arr: np.ndarray, m: int) -> np.ndarray:
    """Extracts the first m elements from a numpy array."""
    return arr[:m]

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a circular right shift of 3 positions to the input array.

    Args:
        input_grid: A 1D NumPy array of shape (12,) containing integers.

    Returns:
        A 1D NumPy array of shape (12,) representing the transformed sequence.
    """
    # Define the shift amount
    shift_amount = 3
    array_length = len(input_grid)

    # Extract the subsequence containing the last 3 elements
    last_part = extract_last_n(input_grid, shift_amount)

    # Extract the subsequence containing the first 9 elements (length - shift_amount)
    first_part = extract_first_m(input_grid, array_length - shift_amount)

    # Concatenate the two parts in the new order: last part first, then first part
    output_grid = np.concatenate((last_part, first_part))

    # Return the resulting array
    return output_grid
