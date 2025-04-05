```python
"""
Performs a right circular shift on a 1D NumPy array. The last element of the input array is moved to the first position, and all other elements are shifted one position to the right.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Moves the last element of a 1D NumPy array to the first position,
    shifting all other elements one position to the right.

    Args:
        input_grid: A 1D NumPy array.

    Returns:
        A new 1D NumPy array with elements shifted right circularly.
    """

    # Get the number of elements in the input array
    num_elements = input_grid.size

    # Handle edge cases: empty or single-element arrays
    if num_elements <= 1:
        return input_grid # No shift needed, return the original array

    # Extract the last element
    last_element = input_grid[-1:] # Slice to keep it as an array

    # Extract all elements except the last one
    remaining_elements = input_grid[:-1]

    # Concatenate the last element (now at the beginning) with the remaining elements
    output_grid = np.concatenate((last_element, remaining_elements))

    return output_grid

```