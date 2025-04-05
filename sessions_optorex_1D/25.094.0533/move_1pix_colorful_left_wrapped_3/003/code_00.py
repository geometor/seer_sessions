"""
Performs a single left rotation on the input 1D NumPy array. It takes the 
first element of the array and moves it to the end, preserving the relative 
order of the other elements.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a single left rotation to the input 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the input array after moving the first 
        element to the end.
    """

    # Get the size of the input array
    size = input_grid.shape[0]

    # Handle edge cases: empty or single-element arrays need no rotation
    if size < 2:
        return input_grid.copy() # Return a copy to avoid modifying the original if needed

    # Extract the first element
    first_element = input_grid[0]

    # Extract the remaining elements (from the second element to the end)
    remaining_elements = input_grid[1:]

    # Create the output array by appending the first element to the remaining elements
    # Note: np.append creates a new array
    output_grid = np.append(remaining_elements, first_element)

    return output_grid