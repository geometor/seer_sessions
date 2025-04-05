import collections

"""
Transforms a sequence of 12 digits based on the pattern of the last 8 digits (the suffix).

1.  The input is a sequence of 12 digits.
2.  The first 4 digits (prefix) are always '0 0 0 0' and remain unchanged.
3.  The last 8 digits (suffix) contain exactly six instances of a single non-zero digit (X) and two instances of the digit 0.
4.  The target pattern for the suffix is defined as 'X X X 0 X X 0 X'.
5.  If the input suffix already matches the target pattern, the output sequence is identical to the input sequence.
6.  If the input suffix does not match the target pattern, the output sequence is constructed by keeping the original prefix ('0 0 0 0') and appending a new suffix rearranged into the target pattern ('X X X 0 X X 0 X').
"""

def find_non_zero_digit(suffix):
  """Finds the unique non-zero digit in the suffix list."""
  for digit in suffix:
    if digit != 0:
      return digit
  # Should not happen based on problem description, but good practice
  return None 

def format_output(output_list):
    """Converts a list of integers to a space-separated string."""
    return " ".join(map(str, output_list))

def parse_input(input_str):
    """Converts a space-separated string of digits to a list of integers."""
    return [int(d) for d in input_str.split()]

def transform(input_str):
    """
    Applies the transformation rule to the input string.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)

    # Separate the prefix and suffix
    prefix = input_list[:4]
    suffix = input_list[4:]

    # Verify prefix is [0, 0, 0, 0] (optional based on strictness)
    # if prefix != [0, 0, 0, 0]:
    #     raise ValueError("Input prefix is not [0, 0, 0, 0]")
        
    # Verify suffix composition (optional based on strictness)
    # counts = collections.Counter(suffix)
    # if len(counts) != 2 or counts[0] != 2 or sum(1 for d in counts if d != 0) != 1:
    #      raise ValueError("Suffix composition is invalid")

    # Identify the non-zero digit (X) in the suffix
    non_zero_x = find_non_zero_digit(suffix)
    if non_zero_x is None:
        # Handle case where suffix is all zeros, though not expected by examples
         return format_output(input_list) 

    # Define the target pattern for the suffix
    target_suffix = [non_zero_x, non_zero_x, non_zero_x, 0, non_zero_x, non_zero_x, 0, non_zero_x]

    # Check if the input suffix matches the target pattern
    if suffix == target_suffix:
        # If it matches, the output is identical to the input
        output_list = input_list
    else:
        # If it doesn't match, construct the output using the prefix and the target suffix
        output_list = prefix + target_suffix

    # Format the output list back into a space-separated string
    return format_output(output_list)
