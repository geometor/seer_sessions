```python
import numpy as np
import math # Although not strictly needed for this specific sorting task

"""
Transforms an input NumPy array of digits (0, 1, 2) into an output string 
where the same digits are sorted in descending numerical order (2s, then 1s, then 0s) 
and formatted as a space-separated string.
"""

def transform(input_grid: np.ndarray) -> str:
    """
    Sorts the digits in the input NumPy array in descending order and returns 
    them as a space-separated string.

    Args:
        input_grid: A 1-dimensional NumPy array containing integer digits (0, 1, or 2).

    Returns:
        A string containing the same digits as the input, sorted in descending
        order (2s, 1s, 0s), and space-separated.
    """
    # 1. Receive the input as a 1-dimensional NumPy array (input_grid).
    # No action needed here, it's the function argument.

    # 2. Sort the elements of the NumPy array in descending numerical order.
    # Use np.sort for ascending order, then reverse the result.
    # Using negative values allows sorting in descending order directly with np.sort
    # but reversing after standard sort is often clearer.
    sorted_array = np.sort(input_grid)[::-1]

    # 3. Convert each integer element in the sorted array into its string representation.
    # Use map(str, ...) for this conversion.
    string_elements = map(str, sorted_array)

    # 4. Join these string representations together, separated by single spaces.
    # Use the join method of strings.
    output_str = " ".join(string_elements)

    # 5. Return the resulting space-separated string.
    return output_str

```