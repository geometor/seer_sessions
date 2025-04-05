"""
Transforms an input string containing 12 space-separated integers by performing a right cyclic shift of 3 positions. 
This is achieved by parsing the string into a list, taking the last 3 elements and prepending them 
to the first 9 elements, and then formatting the result back into a space-separated string.
"""

import numpy as np # Not strictly necessary for this implementation, but potentially useful for similar tasks.

def parse_input_string(input_str):
  """
  Parses a space-separated string of integers into a list of integers.

  Args:
    input_str: The input string.

  Returns:
    A list of integers.
  """
  return [int(x) for x in input_str.split()]

def format_output_list(output_list):
  """
  Formats a list of integers into a space-separated string.

  Args:
    output_list: The list of integers.

  Returns:
    A space-separated string representation of the list.
  """
  return " ".join(map(str, output_list))

def cyclic_shift_right(data_list, shift_amount):
  """
  Performs a right cyclic shift on a list.

  Args:
    data_list: The list to shift.
    shift_amount: The number of positions to shift right.

  Returns:
    A new list with elements shifted cyclically to the right.
  """
  if not data_list:
      return []
  shift_amount = shift_amount % len(data_list) # Ensure shift amount is within list bounds
  # Slice the list into two parts: the last 'shift_amount' elements and the rest
  last_elements = data_list[-shift_amount:]
  first_elements = data_list[:-shift_amount]
  # Concatenate them in the shifted order
  shifted_list = last_elements + first_elements
  return shifted_list

def transform(input_str):
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string representing the transformed sequence, also space-separated.
    """
    # Step 1: Parse the input string into a list of integers.
    parsed_input = parse_input_string(input_str)

    # Step 2 & 3: Identify and separate the parts for shifting (last 3 and first 9)
    # This is handled implicitly by the cyclic_shift_right function.
    
    # Step 4 & 5: Perform the right cyclic shift by 3 positions.
    # Using a helper function for clarity.
    transformed_list = cyclic_shift_right(parsed_input, 3)
    
    # Step 6: Format the transformed list back into a space-separated string.
    output_str = format_output_list(transformed_list)

    # Step 7: Return the result.
    return output_str