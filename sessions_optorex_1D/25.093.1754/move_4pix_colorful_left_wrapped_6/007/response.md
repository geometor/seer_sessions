```python
"""
Rearrange a NumPy array of 12 integers by performing a cyclic left shift. 
The first 4 elements of the input array are moved to the end of the array,
while the remaining 8 elements shift to the beginning.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Applies a cyclic left shift of 4 positions to a NumPy array of length 12.

    Args:
        input_array: A NumPy array of shape (12,) containing integers.

    Returns:
        A NumPy array of shape (12,) containing the rearranged sequence.
    """
    
    # Define the split index - the number of elements to move from front to back
    split_index = 4

    # Validate input shape (optional but good practice for robustness)
    if input_array.shape != (12,):
        raise ValueError(f"Input array must have shape (12,), but got {input_array.shape}")

    # Slice the array to get the first part (elements 0 through 3)
    first_part = input_array[:split_index]
    
    # Slice the array to get the second part (elements 4 through 11)
    second_part = input_array[split_index:]

    # Concatenate the second part followed by the first part to create the output array
    # This effectively moves the first_part to the end.
    output_array = np.concatenate((second_part, first_part))

    # Return the rearranged array
    return output_array

```