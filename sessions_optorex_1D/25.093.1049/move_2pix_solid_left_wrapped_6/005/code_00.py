"""
1. Parse the input string into a sequence (list or array) of 12 integers.
2. Perform a cyclic rotation of the sequence elements 2 positions to the left.
   - This means the element originally at index `i` moves to index `(i - 2) modulo 12`.
   - Equivalently, the first two elements wrap around to become the last two elements.
3. Format the resulting sequence back into a space-separated string.
4. Return the formatted string as the output.
"""

from collections import deque
import numpy as np # Import numpy as the test harness might use numpy arrays

# Helper function to parse the input string
def parse_input(input_str: str) -> list[int]:
  """Parses the space-separated string into a list of integers."""
  return [int(x) for x in input_str.split()]

# Helper function to format the output list
def format_output(output_list: list[int]) -> str:
  """Formats the list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

# Helper function for cyclic left rotation using deque
def rotate_left_deque(seq, n):
  """Rotates a sequence cyclically to the left by n positions using deque."""
  # Robust check for empty sequence (works for lists and numpy arrays)
  if len(seq) == 0:
      return []
  d = deque(seq)
  d.rotate(-n) # Negative rotation for left shift
  return list(d)

def transform(input_str: str) -> str:
    """
    Applies a cyclic left shift of 2 positions to the input sequence represented
    as a space-separated string.

    Args:
        input_str: A string representing a sequence of 12 space-separated integers.

    Returns:
        A string representing the transformed sequence, also space-separated.
    """
    # 1. Parse the input string into a sequence (list) of integers.
    #    The test harness might pass a numpy array, but parsing the string
    #    representation gives us a list initially.
    input_sequence = parse_input(input_str)

    # Define the amount of left shift
    shift_amount = 2

    # 2. Perform a cyclic rotation of the sequence elements 2 positions to the left.
    #    The rotate_left_deque helper handles this efficiently.
    #    It works correctly even if the input `input_sequence` were a numpy array
    #    because deque can be initialized with various iterables.
    output_sequence = rotate_left_deque(input_sequence, shift_amount)

    # 3. Format the resulting sequence back into a space-separated string.
    output_str = format_output(output_sequence)

    # 4. Return the formatted string.
    return output_str