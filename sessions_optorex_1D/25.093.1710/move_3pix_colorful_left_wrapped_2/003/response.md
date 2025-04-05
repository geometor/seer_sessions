```python
import numpy as np

"""
Takes an input sequence (NumPy array of 12 integers), performs a left rotation by 3 positions, and returns the resulting sequence (NumPy array).
This is achieved by splitting the input array into the first 3 elements and the remaining 9 elements, then concatenating the 9-element part followed by the 3-element part.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Performs a left rotation by 3 positions on a 1D NumPy array of 12 integers.

    Args:
        input_grid: A NumPy array of shape (12,) containing integers.

    Returns:
        A NumPy array of shape (12,) representing the input array rotated left by 3 positions.
    """
    
    # Ensure the input is a NumPy array (though the environment likely guarantees this)
    if not isinstance(input_grid, np.ndarray):
         # In a real scenario, might convert or raise error. Assuming it's already an ndarray based on prior errors.
         input_grid = np.array(input_grid) 

    # Check if the input sequence has the expected length (optional but good practice)
    if input_grid.shape != (12,):
        raise ValueError("Input array must have shape (12,)")

    # Extract the first 3 elements
    first_part = input_grid[:3]

    # Extract the remaining 9 elements (from index 3 onwards)
    second_part = input_grid[3:]

    # Construct the output sequence by concatenating the second part followed by the first part
    output_grid = np.concatenate((second_part, first_part))

    return output_grid
```