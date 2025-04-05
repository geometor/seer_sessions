```python
"""
Sorts the elements of an input NumPy array of 12 integers (composed of 0s, 1s, and 2s) in descending order.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Sorts the elements of a NumPy array in descending order.

    Args:
        input_array: A NumPy array containing integers.

    Returns:
        A NumPy array containing the sorted integers in descending order.
    """
    # Use numpy.sort to sort the array in ascending order.
    # Note: np.sort returns a sorted copy, leaving the original array unchanged.
    sorted_ascending = np.sort(input_array)

    # Reverse the sorted array to achieve descending order using slicing [::-1].
    output_array = sorted_ascending[::-1]

    # Return the sorted array.
    return output_array
```