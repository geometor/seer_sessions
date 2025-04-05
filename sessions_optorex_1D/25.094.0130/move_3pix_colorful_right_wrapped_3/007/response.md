```python
"""
Transforms a 1-dimensional NumPy array of 12 integers by rearranging its segments.
The transformation rule is as follows:
1. Divide the input array into three segments based on indices:
    - Segment A: The first 8 elements (indices 0-7).
    - Segment B: The single element at index 8.
    - Segment C: The last 3 elements (indices 9-11).
2. Construct the output array by concatenating these segments in the order: 
   Segment C, then Segment A, and finally Segment B.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Applies the rearrangement transformation to the input NumPy array.

    Args:
        input_array: A NumPy array of shape (12,) containing integers.

    Returns:
        A NumPy array of shape (12,) with elements rearranged according to the rule.
    """

    # Validate input shape (optional but good practice for robustness)
    if input_array.shape != (12,):
        raise ValueError("Input array must have shape (12,)")

    # Step 1: Extract the three segments using NumPy slicing
    # Segment A: The first 8 elements (indices 0 through 7)
    segment_A = input_array[0:8]

    # Segment B: The single element at index 8. 
    # Slicing with [8:9] ensures it remains a 1D array for concatenation.
    segment_B = input_array[8:9] 

    # Segment C: The last 3 elements (indices 9 through 11)
    segment_C = input_array[9:12]

    # Step 2: Construct the output array by concatenating the segments
    # The order of concatenation is C, then A, then B.
    output_array = np.concatenate((segment_C, segment_A, segment_B))

    # Step 3: Return the resulting rearranged array
    return output_array

```