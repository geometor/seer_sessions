```python
"""
Sorts the elements of an input NumPy array containing integers (0, 1, 2) in descending numerical order (2 > 1 > 0).
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Sorts the elements of the input NumPy array in descending order.

    Args:
        input_array: A NumPy array containing integers (0, 1, or 2).
                       Expected to be 1-dimensional based on examples.

    Returns:
        A NumPy array containing the sorted integers in descending order.
    """
    # Sort the input array in ascending order first using numpy's sort function.
    # Note: np.sort returns a *copy* of the array, sorted.
    ascending_sorted_array = np.sort(input_array)

    # Reverse the ascendingly sorted array to get descending order.
    # Slicing with [::-1] creates a reversed view or copy.
    descending_sorted_array = ascending_sorted_array[::-1]

    # Return the array sorted in descending order.
    return descending_sorted_array

```