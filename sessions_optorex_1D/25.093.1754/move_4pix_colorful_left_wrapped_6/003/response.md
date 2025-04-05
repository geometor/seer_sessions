```python
"""
Rearrange a sequence of 12 integers provided as a NumPy array by performing a cyclic left shift. 
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
    
    # Validate input shape (optional but good practice)
    if input_array.shape != (12,):
        raise ValueError("Input array must have shape (12,)")

    # Define the split index
    split_index = 4

    # Slice the array into the first part (first 4 elements)
    first_part = input_array[:split_index]
    
    # Slice the array into the second part (remaining 8 elements)
    second_part = input_array[split_index:]

    # Concatenate the second part followed by the first part to create the output array
    output_array = np.concatenate((second_part, first_part))

    return output_array

```