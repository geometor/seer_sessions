import numpy as np

"""
Sorts a NumPy array of digits (0, 1, 2) according to a custom order: 
elements with value 2 come first, followed by elements with value 0, 
followed by elements with value 1.
"""

def custom_sort_key(digit):
  """
  Defines the custom sorting order for use with sorted(): 2 < 0 < 1.
  Maps input digits to comparable values that reflect the desired order.
  Handles potential integer types from NumPy arrays.
  """
  if digit == 2:
    return 0 # 2 should come first
  elif digit == 0:
    return 1 # 0 should come second
  elif digit == 1:
    return 2 # 1 should come last
  else:
    # Assign a high value for unexpected inputs to place them last,
    # although the problem constraints imply only 0, 1, 2 will be present.
    return 3

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Sorts the input NumPy array based on the custom order 2 -> 0 -> 1.

    Args:
        input_array: A 1D NumPy array containing integers (0, 1, or 2).

    Returns:
        A 1D NumPy array containing the sorted integers according to the custom rule.
    """
    # 1. Receive the input NumPy array. No parsing needed.

    # 2. Sort the elements of the array using the custom sorting key.
    # The sorted() function works on NumPy arrays (iterables) and returns a standard Python list.
    # The custom_sort_key function ensures 2s are treated as smallest, then 0s, then 1s.
    sorted_list = sorted(input_array, key=custom_sort_key)

    # 3. Convert the sorted list back to a NumPy array.
    # Ensure the output type is a NumPy array and preserve the original data type if possible.
    output_array = np.array(sorted_list, dtype=input_array.dtype)

    # 4. Return the resulting sorted NumPy array.
    return output_array