```python
import collections

"""
Rotate the input sequence of 12 integers cyclically to the left by 3 positions.
The first 3 elements of the input sequence become the last 3 elements of the
output sequence. The elements from index 3 to 11 of the input sequence become
the elements from index 0 to 8 of the output sequence.
"""

def parse_input(input_str):
  """Parses the space-separated string into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output(output_list):
  """Formats the list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def rotate_left(sequence, amount):
  """Rotates a list cyclically to the left by a given amount."""
  if not sequence:
    return []
  amount = amount % len(sequence) # Ensure amount is within bounds
  return sequence[amount:] + sequence[:amount]

def transform(input_str):
  """
  Applies a left rotation by 3 positions to the input sequence.

  Args:
    input_str: A string representing a sequence of 12 space-separated integers.

  Returns:
    A string representing the rotated sequence of 12 space-separated integers.
  """
  # Parse the input string into a list of integers
  input_list = parse_input(input_str)

  # Define the rotation amount
  rotation_amount = 3

  # Perform the left rotation
  output_list = rotate_left(input_list, rotation_amount)

  # Format the output list back into a space-separated string
  output_str = format_output(output_list)

  return output_str

```