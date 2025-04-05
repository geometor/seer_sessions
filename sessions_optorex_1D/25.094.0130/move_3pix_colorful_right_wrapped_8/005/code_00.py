"""
Transforms an input sequence of 12 integers by performing a right cyclic shift of 3 positions.
This is achieved by taking the last 3 elements of the input sequence and prepending them 
to the first 9 elements of the input sequence. The input is expected as a NumPy array.
"""

import numpy as np

def cyclic_shift_right(arr, shift_amount):
  """
  Performs a right cyclic shift on a 1D NumPy array.

  Args:
    arr: The 1D NumPy array to shift.
    shift_amount: The number of positions to shift right.

  Returns:
    A new 1D NumPy array with elements shifted cyclically to the right.
  """
  if arr.size == 0:
      return arr
  shift_amount = shift_amount % arr.size # Ensure shift amount is within array bounds
  # Slice the array into two parts: the last 'shift_amount' elements and the rest
  last_elements = arr[-shift_amount:]
  first_elements = arr[:-shift_amount]
  # Concatenate them in the shifted order using numpy's concatenate function
  shifted_arr = np.concatenate((last_elements, first_elements))
  return shifted_arr

def transform(input_grid):
    """
    Applies the right cyclic shift transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array containing 12 integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array (it should be based on previous error)
    # If it wasn't, conversion would be needed: input_grid = np.array(input_grid)
    
    # Validate input shape/size (optional but good practice)
    if input_grid.shape != (12,):
        # This check might need adjustment if the input could be a list sometimes
        # or have different dimensions. Based on the examples and error, (12,) seems likely.
        # raise ValueError(f"Input array must have shape (12,), but got {input_grid.shape}")
        # For flexibility, we might just proceed assuming it's a 1D array of length 12
        pass

    # Define the amount to shift
    shift = 3

    # Perform the right cyclic shift using the helper function
    output_grid = cyclic_shift_right(input_grid, shift)

    # Return the resulting array
    return output_grid