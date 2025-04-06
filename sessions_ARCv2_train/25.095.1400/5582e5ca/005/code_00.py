"""
Transforms an input NumPy array of integers into an output NumPy array of the
same shape. The output array is uniformly filled with the single integer that
appears most frequently (the statistical mode) among all the elements in the
input array.
"""

import numpy as np
from collections import Counter

def _find_mode_from_array(arr: np.ndarray) -> int:
    """Finds the most frequent element (mode) in a NumPy array."""
    # Flatten the array to count all elements regardless of dimension
    flat_elements = arr.flatten()
    # Handle the case of an empty array explicitly
    if flat_elements.size == 0:
        # The desired behavior for an empty input isn't specified by examples.
        # Returning 0, None, or raising an error are options.
        # Let's raise an error as it indicates unexpected input based on examples.
        raise ValueError("Input array cannot be empty.")
        # Alternatively, could return a default like 0 if that makes sense for the context.
        # return 0
    
    # Count frequencies of each element
    counts = Counter(flat_elements)
    
    # Find the element with the highest frequency
    # most_common(1) returns [(mode_element, frequency)]
    mode_element = counts.most_common(1)[0][0]
    return mode_element

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: finds the mode of the input NumPy array
    and returns a new array of the same shape filled with that mode.
    """
    # Check for fundamentally invalid input (e.g., not an array, though type hints help)
    if not isinstance(input_grid, np.ndarray):
        raise TypeError("Input must be a NumPy array.")

    # Handle the empty array case directly in the main function too for clarity
    if input_grid.size == 0:
        # Return an empty array with the same number of dimensions if possible,
        # or just an empty 1D array. Based on examples (3x3), this won't happen.
        # Returning shape=(0,) or similar might be appropriate.
        return np.array([]) # Return an empty 1D array

    # Determine the mode (most frequent element) from the input grid
    mode_value = _find_mode_from_array(input_grid)

    # Get the shape of the input grid
    output_shape = input_grid.shape

    # Create the output grid filled with the mode value
    # np.full is efficient for creating an array filled with a single value
    output_grid = np.full(output_shape, mode_value, dtype=input_grid.dtype) # Preserve input dtype

    # Return the resulting grid
    return output_grid