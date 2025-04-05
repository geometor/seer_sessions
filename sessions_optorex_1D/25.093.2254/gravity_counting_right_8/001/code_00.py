"""
Transforms an input sequence of 12 digits based on the count of non-zero digits.

The transformation rule is as follows:
1. Count the number of non-zero digits in the input sequence (let the count be N).
2. Create an output sequence of 12 digits.
3. The first N digits of the output sequence are set to 1.
4. The remaining (12 - N) digits are set to 0.
"""

import math
import numpy as np
# Add other imports as needed, e.g., from collections import Counter

def count_non_zeros(sequence):
  """Counts the number of non-zero elements in a sequence."""
  count = 0
  for element in sequence:
    if element != 0:
      count += 1
  return count

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string representation of the sequence.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the 12 space-separated digits of the output sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(digit) for digit in input_str.split()]

    # Check if the input list has the expected length (optional but good practice)
    if len(input_list) != 12:
        raise ValueError("Input sequence must contain exactly 12 digits.")

    # Count the non-zero elements in the input list
    non_zero_count = count_non_zeros(input_list)

    # Initialize the output list with zeros
    output_list = [0] * 12

    # Set the first 'non_zero_count' elements to 1
    for i in range(non_zero_count):
        # Ensure we don't try to write past the end of the list
        # (though non_zero_count should always be <= 12)
        if i < 12:
            output_list[i] = 1

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
