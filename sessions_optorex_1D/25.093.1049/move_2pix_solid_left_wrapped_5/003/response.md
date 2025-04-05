```python
import numpy as np

"""
Transforms an input sequence (list or NumPy array) of 12 integers by shifting 
all non-zero elements two positions to the left, with wrap-around. Positions 
not filled by a shifted non-zero element are set to zero.

1. Accept the input sequence (a list or array of 12 integers).
2. Determine the length of the input sequence (n=12).
3. Create a new output sequence of the same length, initialized with zeros.
4. Iterate through the input sequence using index `i` from 0 to n-1.
5. If the element `input_grid[i]` is not zero:
   a. Calculate the target index: `target_index = (i - 2) % n`.
   b. Place the non-zero element into the output sequence at `target_index`: 
      `output_grid[target_index] = input_grid[i]`.
6. Return the completed output sequence.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts non-zero elements of a 12-element sequence two positions to the left,
    wrapping around the ends, and fills remaining positions with zeros.

    Args:
        input_grid: A NumPy array of 12 integers.

    Returns:
        A NumPy array of 12 integers representing the transformed sequence.
    """
    # Get the size of the input grid
    n = len(input_grid)

    # Initialize the output grid with zeros, matching the input type (NumPy array)
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid
    for i in range(n):
        # Check if the current element is non-zero
        if input_grid[i] != 0:
            # Calculate the target index with a left shift of 2 and wrap-around
            target_index = (i - 2) % n
            # Place the non-zero element in the output grid at the target index
            output_grid[target_index] = input_grid[i]

    # Return the transformed grid
    return output_grid

```