import math
import re
import numpy as np
from typing import Sequence, Union

"""
Transforms a sequence of integers by replacing every non-zero integer with 5 while keeping zeros unchanged. The output is returned as a space-separated string.
"""

def transform(input_sequence: Union[Sequence[int], np.ndarray]) -> str:
    """
    Applies the transformation rule to the input sequence of integers.

    Args:
        input_sequence: A sequence (list, tuple, or NumPy array) containing integers.

    Returns:
        A string containing the transformed sequence of space-separated digits.
    """
    # Initialize an empty list to store the transformed integers
    output_digits = []

    # Iterate through each integer (digit) in the input sequence
    for digit in input_sequence:
        # Check if the current integer is equal to 0
        if digit == 0:
            # If the integer is 0, append 0 to the transformed sequence
            output_digits.append(0)
        else:
            # If the integer is not 0, append 5 to the transformed sequence
            output_digits.append(5)

    # Convert each integer in the transformed sequence to its string representation
    output_strings = [str(d) for d in output_digits]

    # Join the resulting strings with a single space character to create the final output string
    output_str = " ".join(output_strings)

    # Return the final output string
    return output_str