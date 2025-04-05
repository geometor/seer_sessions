"""
Transforms an input 1-dimensional NumPy array of digits (0, 1, 2) into an output string 
where the same digits are sorted in descending numerical order (2s first, then 1s, then 0s)
and formatted as a space-separated string.
"""

import numpy as np
# No other specific libraries like math are needed for this task.

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
    #    No explicit action needed here, it's the function argument.

    # 2. Sort the elements of the NumPy array in descending numerical order.
    #    np.sort sorts in ascending order, so we reverse the result using slicing.
    sorted_array = np.sort(input_grid)[::-1]

    # 3. Convert each integer element in the sorted array into its string representation.
    #    Using map() to apply the str function to each element.
    string_elements = map(str, sorted_array)

    # 4. Join these string representations together into a single output string, 
    #    using a single space as the separator.
    output_str = " ".join(string_elements)

    # 5. Return the resulting space-separated string.
    #    Note: The template refers to 'output_grid', but the task clearly requires 
    #    a string output based on the examples. We return the constructed string.
    return output_str
