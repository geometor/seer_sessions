import collections

"""
Transforms an input sequence of integers based on the most frequent non-zero digit.

1.  Examine the input sequence of integers.
2.  Identify all the non-zero integers within the input sequence.
3.  If there are no non-zero integers, the output sequence is identical to the input sequence.
4.  If there are non-zero integers, count the occurrences of each unique non-zero integer.
5.  Determine the non-zero integer that occurs most frequently (the mode).
6.  Construct the output sequence, having the same length as the input sequence.
7.  Iterate through each position of the input sequence:
    *   If the integer at the current position in the input sequence is zero, place a zero at the corresponding position in the output sequence.
    *   If the integer at the current position in the input sequence is non-zero, place the mode (determined in step 5) at the corresponding position in the output sequence.
8.  Return the constructed output sequence as a space-separated string.
"""

def find_non_zero_mode(numbers):
  """
  Finds the most frequent non-zero number in a list.
  Returns None if no non-zero numbers exist or the list is empty.
  """
  non_zeros = [n for n in numbers if n != 0]
  if not non_zeros:
    return None
  
  counts = collections.Counter(non_zeros)
  # Find the number with the maximum count. If there are ties, most_common(1) returns one of them.
  mode, _ = counts.most_common(1)[0]
  return mode

def transform(input_str):
    """
    Applies the transformation rule to the input string sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # Find the mode of the non-zero elements
    mode_digit = find_non_zero_mode(input_list)

    # If there are no non-zero elements, return the original sequence unchanged
    if mode_digit is None:
      # Format the output list back into a space-separated string
      output_str = " ".join(map(str, input_list))
      return output_str

    # Initialize the output list
    output_list = []

    # Iterate through the input list and apply the transformation
    for number in input_list:
        # Keep zeros as they are
        if number == 0:
            output_list.append(0)
        # Replace non-zeros with the mode digit
        else:
            output_list.append(mode_digit)

    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
