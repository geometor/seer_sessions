```python
import numpy as np

"""
Transforms a 1D NumPy array by swapping adjacent pairs of elements.
It iterates through the array with a step of 2. For each pair of elements
at indices `i` and `i+1`, it swaps their positions. If the array has an
odd number of elements, the last element remains in its position relative
to the swapped pairs.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Swaps adjacent elements in a 1D NumPy array.

    Args:
        input_grid: A 1-dimensional NumPy array.

    Returns:
        A new 1-dimensional NumPy array with adjacent elements swapped.
    """
    # Create a copy of the input array to avoid modifying the original
    output_grid = input_grid.copy()

    # Get the number of elements in the array
    n = len(output_grid)

    # Iterate through the array indices with a step of 2
    # Stop before the last element if n is odd, or process the last pair if n is even.
    # The range ensures that i+1 is always a valid index within the loop.
    for i in range(0, n - 1, 2):
        # Swap the element at the current index (i) with the element at the next index (i+1)
        output_grid[i], output_grid[i+1] = output_grid[i+1], output_grid[i]

    # Return the modified array
    return output_grid
```