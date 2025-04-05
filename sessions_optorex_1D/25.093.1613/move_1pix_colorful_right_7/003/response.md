```python
import numpy as np

"""
Transforms an input sequence (NumPy array) of digits by shifting all elements 
one position to the right, inserting a 0 at the beginning, and discarding 
the last element of the original sequence.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the right-shift transformation to the input sequence array.

    Args:
        input_grid: A NumPy array containing single-digit integers.

    Returns:
        A NumPy array containing the transformed sequence.
    """
    # Create a NumPy array containing the single element 0.
    zero_element = np.array([0], dtype=input_grid.dtype)

    # Slice the input grid to get all elements except the last one.
    shifted_elements = input_grid[:-1]

    # Concatenate the zero element with the sliced input elements
    # to form the output grid.
    # Example: input [0, 8, 5, ..., 8, 0] ->
    #          zero_element [0]
    #          shifted_elements [0, 8, 5, ..., 8]
    #          output_grid [0, 0, 8, 5, ..., 8]
    output_grid = np.concatenate((zero_element, shifted_elements))

    return output_grid
```