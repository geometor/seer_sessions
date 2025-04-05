"""
1. Receive the input as a 1D NumPy array of 12 integers.
2. Perform a cyclic left shift on the array by 2 positions using np.roll.
   - np.roll with a negative shift value performs a left shift.
3. Convert each integer element in the shifted array into its string representation.
4. Join these string representations with a single space character in between.
5. Return the resulting space-separated string.
"""

import numpy as np

# Helper function to format a NumPy array into a space-separated string
def format_output_string(arr: np.ndarray) -> str:
  """Converts a 1D NumPy array of numbers into a space-separated string."""
  return " ".join(map(str, arr))

def transform(input_array: np.ndarray) -> str:
  """
  Applies a cyclic left shift of 2 positions to the input NumPy array
  and returns the result as a space-separated string.

  Args:
    input_array: A 1D NumPy array of shape (12,) containing integers.

  Returns:
    A string representing the transformed sequence, space-separated.
  """

  # Define the amount of left shift
  shift_amount = -2 # Negative shift for np.roll corresponds to left shift

  # Perform the cyclic left shift using NumPy's roll function
  # axis=0 is specified for clarity, though it's the default for 1D arrays
  shifted_array = np.roll(input_array, shift=shift_amount, axis=0)

  # Convert the shifted NumPy array to the required output string format
  output_string = format_output_string(shifted_array)

  # Return the formatted string
  return output_string