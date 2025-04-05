```python
import math
import numpy as np
import re # Although not used in the final logic, keeping it for consistency if future regex needed

"""
Moves all zeros in the input sequence to the beginning, while preserving the relative order of the non-zero elements. The input is assumed to be a sequence (like a list or NumPy array) of digits.
"""

def transform(input_sequence):
    """
    Rearranges a sequence of digits by moving all zeros to the front,
    maintaining the relative order of the non-zero digits.

    Args:
        input_sequence: A list or array-like sequence of integers (digits 0-9).

    Returns:
        A new list containing the rearranged sequence of digits.
    """

    # 1. Initialize lists to store zero and non-zero elements
    zeros_list = []
    non_zeros_list = []

    # 2. Iterate through the input sequence
    for digit in input_sequence:
        # 3. Partition elements based on value
        if digit == 0:
            # Append zeros to the zeros list
            zeros_list.append(digit)
        else:
            # Append non-zeros to the non-zeros list, preserving order
            non_zeros_list.append(digit)

    # 4. Concatenate the lists: zeros first, then non-zeros
    output_sequence = zeros_list + non_zeros_list

    # 5. Return the rearranged sequence
    return output_sequence
```