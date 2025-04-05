```python
"""
Parses a string of space-separated integers (0, 1, 2), sorts the integers in non-decreasing order, and returns the sorted sequence as a space-separated string.
"""

import collections # Although not strictly needed for basic sort, keeping it in case counting becomes relevant later or for alternative implementations.

def parse_input_string(input_str):
  """Parses a space-separated string into a list of integers."""
  if not input_str: # Handle empty input string
      return []
  try:
      # Split the string by spaces and convert each part to an integer
      return [int(x) for x in input_str.strip().split()]
  except ValueError:
      # Handle cases where the string might contain non-integer values
      # For this problem context, we might assume valid input, but good practice to consider.
      print(f"Warning: Input string '{input_str}' contains non-integer values or incorrect format.")
      # Decide on error handling: return empty list, raise exception, or filter valid numbers?
      # Let's filter for now, assuming the task implies focusing on valid integers found.
      valid_ints = []
      for x in input_str.strip().split():
          try:
              valid_ints.append(int(x))
          except ValueError:
              continue # Skip non-integer parts
      return valid_ints


def format_output_string(output_list):
  """Formats a list of integers into a space-separated string."""
  # Convert each integer in the list to its string representation
  # Join these strings with a single space in between
  return " ".join(map(str, output_list))

def transform(input_str):
  """
  Transforms an input string of space-separated integers by sorting them.

  Args:
    input_str: A string containing space-separated integers (expected: 0, 1, 2).

  Returns:
    A string containing the same integers sorted in non-decreasing order,
    separated by spaces.
  """

  # Step 1: Parse the input string into a list of integers.
  int_list = parse_input_string(input_str)

  # Step 2: Sort the list of integers in non-decreasing (ascending) order.
  # Python's built-in sort is efficient and suitable here.
  int_list.sort()

  # Step 3: Format the sorted list back into a space-separated string.
  output_str = format_output_string(int_list)

  # Step 4: Return the resulting formatted string.
  return output_str
```