import numpy as np
import math # common math library

"""
Transforms an input string of space-separated integers by:
1. Parsing the string into a list of integers.
2. Creating a new list containing elements from the input list starting from index 2 (the third element) to the end.
3. Appending two integer zeros (0, 0) to this new list.
4. Formatting the resulting list back into a space-separated string.
"""

# Helper function to parse the input string
def parse_input_string(input_str):
  """Converts a space-separated string of integers into a list of integers."""
  # Handle potential empty input or leading/trailing spaces
  if not input_str.strip():
      return []
  return [int(x) for x in input_str.strip().split()]

# Helper function to format the output list
def format_output_list(output_list):
  """Converts a list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def transform(input_str):
    """
    Applies a left shift of 2 positions to the sequence represented by input_str,
    padding the end with two zeros, and returns the result as a string.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing space-separated integers representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers.
    input_list = parse_input_string(input_str)

    # Handle cases where the input list has fewer than 2 elements
    if len(input_list) <= 2:
        # If 2 or fewer elements, shifting leaves an empty list.
        # We need to pad with two zeros to match the observed behavior.
        # The original length was maintained in examples, so the output length
        # should technically match the input if possible. However, the strict
        # rule is 'shift from index 2, append two zeros'.
        # For input length N, output is N-2 elements + 2 zeros = N elements.
        # If N=2, output is 0 elements + 2 zeros = 2 elements.
        # If N=1, output is 0 elements + 2 zeros = 2 elements.
        # If N=0, output is 0 elements + 2 zeros = 2 elements.
        # Let's recalculate padding based on original length for consistency.
        original_length = len(input_list)
        shifted_part = [] # Empty if len <= 2
    else:
        # 2. Create a new list by taking a slice starting from index 2.
        shifted_part = input_list[2:]
        original_length = len(input_list) # Store original length

    # 3. Append two integer zeros (0, 0) to the end of this new list.
    # The requirement is specifically to append *two* zeros.
    output_list = shifted_part + [0, 0]

    # 4. Format the resulting list back into a space-separated string.
    output_str = format_output_list(output_list)

    # 5. Return the formatted output string.
    return output_str