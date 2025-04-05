import collections
import numpy as np # Import numpy for potential array input handling

"""
Transforms a sequence of single-digit integers. It identifies contiguous segments of non-zero numbers,
finds the most frequent number (mode) within each segment, and replaces all numbers in that segment
with the mode. Zeros act as delimiters between segments and remain unchanged in their positions.
"""

def find_mode(segment):
  """
    Finds the most frequent element (mode) in a list of numbers.
    If there are ties, it returns the element that appears first among the most frequent ones
    based on Counter's behavior (usually the one encountered first in the segment).

    Args:
        segment: A list of non-zero integers.

    Returns:
        The most frequent integer in the segment. Returns None if the segment is empty.
  """
  if not segment:
    return None
  # Count occurrences of each number
  counts = collections.Counter(segment)
  # Find the number with the highest count
  # most_common(1) returns a list containing one tuple: [(mode, count)]
  mode = counts.most_common(1)[0][0]
  return mode

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of single-digit integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a standard Python list for consistent iteration and comparison
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Make a copy to avoid modifying the original input if it's mutable
        input_list = list(input_sequence) 

    # Initialize the list to store the final output sequence
    output_sequence = []
    # Initialize a temporary list to hold the current segment of non-zero numbers
    current_segment = []

    # Iterate through each number in the input list
    for number in input_list:
        # Check if the current number is a zero (delimiter)
        # This comparison should now work reliably as number is a Python int
        if number == 0:
            # If a non-zero segment was being built, process it
            if current_segment:
                # Find the mode of the completed segment
                mode = find_mode(current_segment)
                # Create the transformed segment (a list of the mode repeated)
                transformed_segment = [mode] * len(current_segment)
                # Add the transformed segment to the output list
                output_sequence.extend(transformed_segment)
                # Reset the temporary segment list
                current_segment = []
            # Add the zero to the output list (zeros remain unchanged)
            output_sequence.append(0)
        # If the current number is not zero
        else:
            # Add the non-zero number to the current segment being built
            current_segment.append(number)

    # After the loop, check if there's a pending segment
    # (This handles cases where the input sequence doesn't end with 0)
    if current_segment:
        # Find the mode of the final segment
        mode = find_mode(current_segment)
        # Create the transformed final segment
        transformed_segment = [mode] * len(current_segment)
        # Add the final transformed segment to the output list
        output_sequence.extend(transformed_segment)

    # Return the complete transformed sequence as a list
    # (The testing environment might expect a specific type like numpy array,
    # but returning a list is generally compatible and aligns with the core logic)
    return output_sequence