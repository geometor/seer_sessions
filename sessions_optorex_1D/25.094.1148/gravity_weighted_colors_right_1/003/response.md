```python
"""
Sorts the elements of an input sequence of 12 integers (composed of 0s, 1s, and 2s) in descending order.
"""

import numpy as np

def transform(input_sequence):
    """
    Sorts a sequence of integers in descending order.

    Args:
        input_sequence: A sequence (e.g., list or numpy array) of integers.

    Returns:
        A numpy array containing the sorted integers in descending order.
    """

    # The input might be a list or a numpy array.
    # Python's built-in sorted() function works on various sequence types
    # and returns a new list.
    # We specify reverse=True for descending order.
    sorted_list = sorted(input_sequence, reverse=True)

    # Convert the resulting sorted list to a numpy array for consistency
    # with the typical data structures used in such environments.
    output_sequence = np.array(sorted_list)

    return output_sequence
```