```python
import numpy as np

"""
Transforms an input sequence (NumPy array) of 12 digits by performing a 
right shift of 4 positions. The leftmost 4 positions of the output sequence 
are filled with the padding value 0. The first 8 elements of the input 
sequence occupy positions 4 through 11 (indices 4-11) in the output sequence.
The last 4 elements of the input are effectively discarded.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a right shift of 4 positions with zero-padding to the input sequence.

    Args:
        input_grid: A NumPy array of 12 digits.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Define the shift amount and padding value
    shift_amount = 4
    padding_value = 0
    
    # Determine the length of the input grid
    grid_length = len(input_grid)

    # Calculate the number of elements to keep from the input
    elements_to_keep = grid_length - shift_amount

    # Create the padding array
    # Ensure padding has the same dtype as input if necessary, 
    # though 0 usually works fine for numeric types.
    padding = np.full(shift_amount, padding_value, dtype=input_grid.dtype) 

    # Select the portion of the input grid that will be shifted
    # These are the first 'elements_to_keep' elements (indices 0 to elements_to_keep-1)
    shifted_part = input_grid[:elements_to_keep]

    # Concatenate the padding and the shifted part to form the output grid
    output_grid = np.concatenate((padding, shifted_part))

    return output_grid
```