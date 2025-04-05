import numpy as np

"""
Moves the last element of the input sequence to the beginning, effectively performing a right cyclic shift by one position.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input sequence (NumPy array) by moving the last element to the front.

    Args:
        input_grid: A NumPy array representing the sequence of numbers.

    Returns:
        A NumPy array representing the transformed sequence.
    """

    # Check if the input array is empty or has only one element
    if input_grid.size <= 1:
        return input_grid.copy() # Return a copy to avoid modifying the original if it's the same

    # Identify the last element
    last_element = input_grid[-1:] # Use slicing to keep it as an array dimension

    # Identify the remaining elements (all except the last)
    remaining_elements = input_grid[:-1]

    # Concatenate the last element at the beginning of the remaining elements
    output_grid = np.concatenate((last_element, remaining_elements))

    return output_grid
