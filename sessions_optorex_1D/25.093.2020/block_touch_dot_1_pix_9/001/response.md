```python
"""
Transforms a sequence of 12 integers based on specific patterns involving the numbers 0 and 2 near the end of the sequence.

1. If the second-to-last element is 0 and the last element is 2, move the 0 from the second-to-last position to the beginning of the sequence.
2. If the third-to-last element is 2 and the second-to-last element is 0, move the 0 from the second-to-last position to the end of the sequence.
3. Otherwise, the sequence remains unchanged.
"""

import re # Although not strictly needed for this logic, importing common libraries as per instruction.
import math

def _parse_input(input_str):
  """Converts the input string into a list of integers."""
  return [int(x) for x in input_str.strip().split()]

def _format_output(output_list):
  """Converts the list of integers back into a space-separated string."""
  return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string representing the transformed sequence, with integers separated by spaces.
    """
    # Parse the input string into a list of integers
    input_list = _parse_input(input_str)
    n = len(input_list)

    # Initialize output list as a copy of the input list
    output_list = list(input_list) # Make a copy to modify

    # Check condition 1: penultimate is 0 and ultimate is 2
    # Indices are n-2 and n-1 (for length 12, indices 10 and 11)
    if n >= 2 and output_list[n - 2] == 0 and output_list[n - 1] == 2:
        # Remove the 0 from the penultimate position
        val_to_move = output_list.pop(n - 2)
        # Insert the 0 at the beginning
        output_list.insert(0, val_to_move)
        # Format and return the result
        return _format_output(output_list)

    # Check condition 2: antepenultimate is 2 and penultimate is 0
    # Indices are n-3 and n-2 (for length 12, indices 9 and 10)
    elif n >= 3 and output_list[n - 3] == 2 and output_list[n - 2] == 0:
        # Remove the 0 from the penultimate position
        val_to_move = output_list.pop(n - 2)
        # Append the 0 to the end
        output_list.append(val_to_move)
        # Format and return the result
        return _format_output(output_list)

    # Otherwise (neither condition met), return the original sequence formatted as a string
    else:
        return _format_output(output_list)

```