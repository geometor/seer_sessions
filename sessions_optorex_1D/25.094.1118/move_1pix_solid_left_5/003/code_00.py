"""
Transforms an input sequence (list or NumPy array) of 12 integers by performing a left cyclic shift by one position. The first element is moved to the last position, and all other elements shift one position to the left.
"""

import numpy as np
from typing import List, Union

def transform(input_sequence: Union[List[int], np.ndarray]) -> Union[List[int], np.ndarray]:
    """
    Performs a left cyclic shift on the input sequence by one position.

    Args:
        input_sequence: A list or NumPy array of integers.

    Returns:
        A list or NumPy array representing the transformed sequence.
    """

    # Handle potential NumPy array input by converting to list for consistent manipulation
    # (Alternatively, could use np.roll if input is guaranteed to be ndarray)
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Assume it's already list-like or directly usable as a list
        input_list = list(input_sequence) 

    # Handle the edge case of an empty input sequence
    if not input_list:
        # Return in the original format if possible, otherwise empty list
        return np.array([]) if isinstance(input_sequence, np.ndarray) else []

    # Extract the first element
    first_element = input_list[0]

    # Create a new list containing elements from the second position onwards
    shifted_part = input_list[1:]

    # Append the first element to the end of the shifted part
    output_list = shifted_part + [first_element]

    # Return in the original format if it was ndarray, otherwise as list
    return np.array(output_list) if isinstance(input_sequence, np.ndarray) else output_list