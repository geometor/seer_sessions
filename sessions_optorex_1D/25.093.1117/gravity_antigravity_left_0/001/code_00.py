import collections

"""
Sorts a sequence of digits (0, 1, 2) according to a custom order: 2s first, then 0s, then 1s.
The input is a string of space-separated digits.
The output is a string of space-separated digits sorted according to the custom rule.
"""

# No external libraries needed beyond standard collections

def custom_sort_key(digit):
  """
  Defines the custom sorting order: 2 < 0 < 1.
  Maps digits to sortable values.
  """
  if digit == 2:
    return 0 # 2 comes first
  elif digit == 0:
    return 1 # 0 comes second
  elif digit == 1:
    return 2 # 1 comes last
  else:
    # Handle unexpected values if necessary, though the problem implies only 0, 1, 2
    return 3 

def transform(input_str):
    """
    Sorts the input sequence of digits based on the custom order 2 -> 0 -> 1.

    Args:
        input_str: A string containing space-separated digits (0, 1, or 2).

    Returns:
        A string containing the sorted digits, space-separated.
    """
    # 1. Receive the input sequence and parse it
    # Split the input string by spaces and convert each part to an integer
    input_digits = [int(d) for d in input_str.split()]

    # 2. Sort the digits using the custom key
    # The custom_sort_key function dictates that 2s are smallest, then 0s, then 1s
    sorted_digits = sorted(input_digits, key=custom_sort_key)

    # 3. Construct the output sequence string
    # Convert the sorted integers back to strings
    output_digits_str = [str(d) for d in sorted_digits]
    
    # Join the string digits with spaces
    output_str = " ".join(output_digits_str)

    # 4. Return the resulting sequence string
    return output_str
