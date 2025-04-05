```python
"""
Transforms an input 1D NumPy array of integers by performing a left shift by one position. 
The integer at the first position (index 0) is discarded, and the integer 0 is appended 
to the end of the array to maintain the original length.
"""

import numpy as np

def transform(input_arr: np.ndarray) -> np.ndarray:
    """
    Applies a left shift transformation to a 1D NumPy array of integers.

    Args:
        input_arr: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the transformed sequence.
    """
    # Select elements from the second element (index 1) to the end
    # This effectively discards the element at index 0
    shifted_part = input_arr[1:]

    # Append the integer 0 to the end of the selected elements
    # Ensure the appended value is an integer to match the likely dtype
    output_arr = np.append(shifted_part, 0)

    # Return the resulting array
    return output_arr
```