```python
"""
Transforms the input sequence (a 1D NumPy array of 12 integers) by shifting all 
elements two positions to the left, effectively discarding the first two elements, 
and appending two zeros at the end. The final output is a string of 
space-separated integers.
"""

import numpy as np

def format_output(output_list):
  """Formats a list/array of numbers into a string of space-separated integers."""
  return ' '.join(map(str, output_list))

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the left shift and padding transformation.

    Args:
        input_grid: A 1D NumPy array of 12 integers.

    Returns:
        A string representation of the transformed sequence, with elements
        separated by spaces.
    """
    # Define the amount to shift/discard from the left
    shift_amount = 2
    # Define the value to pad with
    pad_value = 0

    # Take elements starting from the index `shift_amount` to the end
    # This effectively discards the first `shift_amount` elements.
    shifted_part = input_grid[shift_amount:]

    # Create the padding array
    # Using np.full ensures the padding has the same dtype if needed,
    # though here it's just zeros.
    padding = np.full(shift_amount, pad_value, dtype=input_grid.dtype)

    # Concatenate the shifted part with the padding
    output_sequence = np.concatenate((shifted_part, padding))

    # Format the resulting NumPy array into a space-separated string
    output_str = format_output(output_sequence)

    # Return the formatted string
    return output_str
```