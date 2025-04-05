import math
import numpy as np # Although not strictly needed for the final logic, it might be the input type

"""
Constructs a binary sequence, formatted as a space-separated string, based on an input sequence of integers.
The length of the output sequence matches the length of the input sequence.
The number of '1's at the beginning of the output sequence equals the count of non-zero elements in the input sequence.
The remaining elements of the output sequence are '0's.
"""

def count_non_zeros(sequence):
  """Counts the number of non-zero elements in a sequence (list or array)."""
  count = 0
  for x in sequence:
    if x != 0:
      count += 1
  return count

def format_output_list(int_list):
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, int_list))

def transform(input_sequence) -> str:
    """
    Transforms an input sequence of integers (list or numpy array) into an output string
    of space-separated binary digits (0s and 1s). The number of 1s in the output
    corresponds to the count of non-zero numbers in the input.
    """
    # Determine the total length of the input sequence
    n = len(input_sequence)

    # Count the number of non-zero elements in the input sequence
    c = count_non_zeros(input_sequence)

    # Initialize the output list
    output_list = []

    # Add 'c' number of 1s to the output list
    # Using list multiplication for conciseness
    output_list.extend([1] * c)

    # Add 'n - c' number of 0s to the output list
    # Using list multiplication for conciseness
    output_list.extend([0] * (n - c))

    # Format the output list into a space-separated string
    output_str = format_output_list(output_list)

    # Return the final formatted string
    return output_str