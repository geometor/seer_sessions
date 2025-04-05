```python
import numpy as np # Import numpy, although standard list operations are sufficient
import math
import re # Import re, although not used in this specific logic

"""
Rearranges a sequence of digits by moving all zero (0) elements to the beginning of the sequence, while preserving the original relative order of all non-zero elements.
"""

def transform(input_sequence):
    """
    Moves all zeros in the input sequence to the beginning, preserving the relative order of non-zero elements.

    Args:
        input_sequence: A list or array-like sequence of integers (digits 0-9).

    Returns:
        A new list containing the rearranged sequence of digits.
    """

    # 1. Initialize lists to store zero and non-zero elements
    zeros_group = []
    non_zeros_group = []

    # 2. Iterate through the input sequence, processing one digit at a time.
    #    This loop correctly handles iterating over elements whether input_sequence
    #    is a list or a NumPy array.
    for digit in input_sequence:
        # 3. For each individual digit examined:
        #    Check if the digit's value is exactly 0.
        if digit == 0:
            # If the digit is 0, append it to the zeros_group.
            zeros_group.append(digit)
        else:
            # If the digit is not 0, append it to the non_zeros_group.
            non_zeros_group.append(digit)

    # 4. Combine the two groups by concatenating the zeros_group
    #    followed by the non_zeros_group.
    output_sequence = zeros_group + non_zeros_group

    # 5. Return the rearranged sequence.
    #    (Formatting to string is assumed to happen outside this function based on problem description)
    return output_sequence
```