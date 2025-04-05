import math # math and science libraries are available
# numpy, pandas, etc. could be imported if needed

"""
Transformation Rule: Given a sequence of digits, find the index of the first non-zero digit. Insert a '0' digit at that specific index within the sequence. If the sequence contains only zeros, insert the '0' at the beginning (index 0).
"""

def find_first_non_zero_index(digit_list):
  """
  Finds the index of the first non-zero digit in a list.
  
  Args:
    digit_list: A list of integers.

  Returns:
    The index of the first non-zero digit. Returns 0 if all digits are zero.
  """
  for index, digit in enumerate(digit_list):
    if digit != 0:
      return index
  # If no non-zero digit is found, return 0 as per the refined understanding
  # (inserting at the beginning if all are zeros, similar to when the first is non-zero)
  return 0

def transform(input_str: str) -> str:
    """
    Transforms the input string sequence by inserting a '0' before the first non-zero digit.

    Args:
      input_str: A string containing space-separated single digits.

    Returns:
      A string containing the transformed sequence, also space-separated.
    """
    
    # Parse the input string into a list of integers
    # Handle potential empty strings or formatting errors if necessary,
    # but based on examples, assume valid input.
    if not input_str.strip():
        return "" # Return empty if input is empty or whitespace
        
    input_digits = [int(d) for d in input_str.split()]

    # Find the index where the '0' should be inserted
    insertion_index = find_first_non_zero_index(input_digits)

    # Create the output list by inserting '0' at the determined index
    # Create a copy to avoid modifying the original list if it were needed elsewhere
    output_digits = list(input_digits) 
    output_digits.insert(insertion_index, 0)

    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_digits))

    return output_str
