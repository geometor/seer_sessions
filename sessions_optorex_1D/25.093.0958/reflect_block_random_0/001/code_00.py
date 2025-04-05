import math

"""
Reverses the sub-sequence of digits located between the first and last non-zero digits (inclusive) in the input sequence, while preserving the position of any leading or trailing zeros.
If no non-zero digits exist, or only one exists, the sequence remains unchanged.
"""

def find_first_non_zero(data):
  """Finds the index of the first non-zero element."""
  for i, x in enumerate(data):
    if x != 0:
      return i
  return -1 # Indicate no non-zero element found

def find_last_non_zero(data):
  """Finds the index of the last non-zero element."""
  for i in range(len(data) - 1, -1, -1):
    if data[i] != 0:
      return i
  return -1 # Indicate no non-zero element found

def transform(input_str):
    """
    Transforms the input sequence string according to the described rule.

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string representing the transformed sequence, with digits separated by spaces.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # 1. & 2. Identify the index of the first non-zero digit
    start_index = find_first_non_zero(input_list)

    # If no non-zero digit exists, return the original sequence as a string
    if start_index == -1:
      return input_str

    # 3. Identify the index of the last non-zero digit
    end_index = find_last_non_zero(input_list)

    # If start and end are the same (only one non-zero), no reversal needed
    if start_index == end_index:
        return input_str

    # 4. Define the sub-sequence to be reversed
    sub_sequence_to_reverse = input_list[start_index : end_index + 1]

    # 5. Reverse the order of the digits within this sub-sequence
    reversed_sub_sequence = sub_sequence_to_reverse[::-1]

    # 6. Construct the output sequence
    # Get leading elements (zeros or empty if first element is non-zero)
    leading_part = input_list[:start_index]
    # Get trailing elements (zeros or empty if last element is non-zero)
    trailing_part = input_list[end_index + 1:]

    # Combine the parts
    output_list = leading_part + reversed_sub_sequence + trailing_part

    # 7. Return the constructed output sequence as a space-separated string
    return " ".join(map(str, output_list))
