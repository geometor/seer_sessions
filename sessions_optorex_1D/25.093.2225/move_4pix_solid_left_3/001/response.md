```python
import math

"""
Treat the input sequence of digits as a list or array. Shift all elements of the sequence 4 positions to the left. Discard the first 4 elements that are shifted beyond the beginning of the sequence boundary. Fill the 4 empty positions created at the right end of the sequence with the digit 0. The resulting sequence is the output.
"""

def parse_input(input_str):
  """Converts a space-separated string of digits into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output(output_list):
  """Converts a list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def shift_left(sequence, shift_amount, fill_value=0):
  """
  Shifts a list to the left by a specified amount, filling the end with a value.

  Args:
    sequence: The list to shift.
    shift_amount: The number of positions to shift left.
    fill_value: The value to fill the empty positions at the end.

  Returns:
    A new list representing the shifted sequence.
  """
  if shift_amount <= 0:
      return list(sequence) # No shift or invalid shift amount
  if shift_amount >= len(sequence):
      return [fill_value] * len(sequence) # Shifted entirely out

  # Take the part of the sequence starting from the shift_amount index
  shifted_part = sequence[shift_amount:]
  # Create the fill part
  fill_part = [fill_value] * shift_amount
  # Concatenate them
  return shifted_part + fill_part


def transform(input_str):
    """
    Applies a left shift of 4 positions to the input sequence of digits,
    filling the end with zeros.

    Args:
        input_str: A string representing the input sequence of space-separated digits.

    Returns:
        A string representing the transformed sequence of space-separated digits.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)

    # Define the shift amount
    shift_amount = 4

    # Define the fill value
    fill_value = 0

    # Perform the left shift operation
    output_list = shift_left(input_list, shift_amount, fill_value)

    # Format the resulting list back into a space-separated string
    output_str = format_output(output_list)

    return output_str

```