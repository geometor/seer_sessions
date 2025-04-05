```python
import numpy as np

"""
Transforms an input 1D NumPy array of 12 integers by dividing it into three chunks of 4 integers each 
and rearranging these chunks. The output array is formed by concatenating the second chunk, 
the third chunk, and then the first chunk from the original input array.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Rearranges chunks of a 12-integer NumPy array.

    Args:
        input_grid: A 1D NumPy array containing 12 integers.

    Returns:
        A 1D NumPy array containing the rearranged 12 integers.
    """

    # Ensure the input is a NumPy array (it should be based on the environment)
    # No explicit conversion needed if the input is guaranteed to be ndarray

    # Check if the input array has the expected length
    if input_grid.shape != (12,):
        # Although the problem description implies fixed size, adding a check is good practice.
        # In a real scenario, might raise ValueError or handle differently.
        # For this contest, assume input is always valid shape (12,).
        pass # Assume valid input shape for now

    # Divide the input array into three chunks of 4 integers each using slicing
    chunk_1 = input_grid[0:4]  # First 4 elements (indices 0, 1, 2, 3)
    chunk_2 = input_grid[4:8]  # Middle 4 elements (indices 4, 5, 6, 7)
    chunk_3 = input_grid[8:12] # Last 4 elements (indices 8, 9, 10, 11)

    # Construct the output array by concatenating the chunks
    # in the order: chunk 2, chunk 3, chunk 1
    # The tuple (chunk_2, chunk_3, chunk_1) specifies the order of concatenation
    output_grid = np.concatenate((chunk_2, chunk_3, chunk_1))

    # Return the constructed NumPy array
    return output_grid
```