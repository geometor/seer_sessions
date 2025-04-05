import collections

"""
Transforms a sequence of single-digit integers based on segment analysis.

1. Iterate through the input sequence of digits.
2. Identify contiguous segments (runs) of non-zero digits. Zeros act as separators.
3. For each non-zero segment:
   a. Find the most frequent digit (mode) within that segment.
   b. Replace all digits in that segment with the calculated mode.
4. Zeros remain unchanged in their original positions.
5. Reconstruct the sequence with the transformed segments and original zeros.
"""

def find_mode(segment):
  """
    Finds the most frequent element (mode) in a list of numbers.
    If there are ties, it returns the element that appears first among the most frequent ones
    based on Counter's behavior (usually the one encountered first in the segment).
    """
  if not segment:
    return None
  # Count occurrences of each number
  counts = collections.Counter(segment)
  # Find the number with the highest count
  # most_common(1) returns a list containing one tuple: [(mode, count)]
  mode = counts.most_common(1)[0][0]
  return mode

def transform(input_str):
  """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing the transformed space-separated sequence.
    """
  # Parse the input string into a list of integers
  input_sequence = [int(x) for x in input_str.split()]
  output_sequence = []
  current_segment = []

  # Iterate through the input sequence
  for number in input_sequence:
    if number == 0:
      # If we were processing a non-zero segment, finalize it
      if current_segment:
        # Find the mode of the completed segment
        mode = find_mode(current_segment)
        # Create the transformed segment filled with the mode
        transformed_segment = [mode] * len(current_segment)
        # Add the transformed segment to the output
        output_sequence.extend(transformed_segment)
        # Reset the current segment
        current_segment = []
      # Add the zero to the output
      output_sequence.append(0)
    else:
      # Add the non-zero number to the current segment
      current_segment.append(number)

  # After the loop, check if there's a pending segment (if the sequence didn't end with 0)
  if current_segment:
    mode = find_mode(current_segment)
    transformed_segment = [mode] * len(current_segment)
    output_sequence.extend(transformed_segment)

  # Format the output sequence back into a space-separated string
  return " ".join(map(str, output_sequence))
