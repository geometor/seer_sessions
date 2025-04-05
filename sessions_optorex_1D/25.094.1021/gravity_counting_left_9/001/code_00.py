import collections

"""
Transforms an input string of 12 space-separated digits into an output string of 12 space-separated digits.
The transformation rule is as follows:
1. Count the number of '0' digits in the input string. Let this be N.
2. Count the number of non-zero digits (1-9) in the input string. Let this be M.
3. The output string consists of N '0's followed by M '1's, separated by spaces.
"""

def count_digits(digit_list):
  """Counts the occurrences of '0' and non-zero digits in a list."""
  zero_count = 0
  non_zero_count = 0
  for digit in digit_list:
    if digit == '0':
      zero_count += 1
    else:
      non_zero_count += 1
  return zero_count, non_zero_count

def transform(input_str):
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing 12 space-separated '0's and '1's based on the rule.
    """
    # Parse the input string into a list of digit strings
    input_digits = input_str.split(' ')

    # Count the number of zeros and non-zeros
    # zero_count = input_digits.count('0') # Alternative using list.count
    # non_zero_count = len(input_digits) - zero_count # Alternative calculation
    zero_count, non_zero_count = count_digits(input_digits)

    # Construct the output list
    # Create a list with N '0's
    output_zeros = ['0'] * zero_count
    # Create a list with M '1's
    output_ones = ['1'] * non_zero_count
    # Concatenate the two lists
    output_digits = output_zeros + output_ones

    # Format the output list into a space-separated string
    output_str = ' '.join(output_digits)

    return output_str
