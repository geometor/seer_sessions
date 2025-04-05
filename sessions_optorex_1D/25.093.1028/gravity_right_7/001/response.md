```python
import math
import numpy as np
import re

"""
Identifies all zero digits and all non-zero digits in the input sequence.
Constructs the output sequence by concatenating all identified zero digits followed by all identified non-zero digits, preserving the original relative order of the non-zero digits.
"""

def transform(input_str: str) -> str:
    """
    Moves all zeros in the input sequence to the beginning, preserving the relative order of non-zero elements.

    Args:
        input_str: A string containing space-separated single digits.

    Returns:
        A string containing space-separated single digits with zeros moved to the front.
    """

    # 1. Read the input sequence of digits.
    # Convert the space-separated string into a list of integers.
    try:
        input_digits = [int(d) for d in input_str.split()]
    except ValueError:
        # Handle potential errors if the input string contains non-digits
        print(f"Error: Input string '{input_str}' contains non-digit characters.")
        return "" # Or raise an exception

    # 2. Create two empty lists: one for zero digits and one for non-zero digits.
    zeros_list = []
    non_zeros_list = []

    # 3. Iterate through the input sequence, digit by digit.
    # 4. For each digit:
    #    *   If the digit is 0, append it to the zeros_list.
    #    *   If the digit is not 0, append it to the non_zeros_list.
    for digit in input_digits:
        if digit == 0:
            zeros_list.append(digit)
        else:
            non_zeros_list.append(digit)

    # 5. Concatenate the zeros_list and the non_zeros_list to form the final output sequence.
    output_digits = zeros_list + non_zeros_list

    # 6. Format the output sequence as a space-separated string of digits.
    output_str = " ".join(map(str, output_digits))

    return output_str

```