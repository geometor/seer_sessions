import collections # Useful for counting, although basic list.count() suffices here.
import numpy as np # Not strictly needed for this logic, but available.

"""
Transforms an input sequence of 12 space-separated integers.
Counts the total number of zeros (N) in the input sequence.
Generates an output sequence of 12 integers consisting of N zeros
followed by (12-N) ones, formatted as a space-separated string.
"""

# Helper function to count a specific value in a list
def count_value(data_list, value_to_count):
  """Counts occurrences of a specific value in a list."""
  count = 0
  for item in data_list:
    if item == value_to_count:
      count += 1
  return count
  # Alternatively, using built-in method:
  # return data_list.count(value_to_count)

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing 12 space-separated integers (0-9).

    Returns:
        A string containing 12 space-separated integers (0 or 1),
        representing the transformed sequence.
    """

    # Define constants
    TARGET_LENGTH = 12
    VALUE_TO_COUNT = 0
    OUTPUT_ZERO = 0
    OUTPUT_ONE = 1
    SEPARATOR = " "

    # 1. Parse the input string into a list of integers.
    # Example: "5 8 2 0 6 0 2 6 0 1 4 0" -> [5, 8, 2, 0, 6, 0, 2, 6, 0, 1, 4, 0]
    try:
        input_sequence = [int(x) for x in input_str.split(SEPARATOR)]
    except ValueError:
        # Handle potential errors if input isn't correctly formatted integers
        print(f"Error: Input string '{input_str}' contains non-integer values.")
        # Depending on requirements, could raise error or return default/error string
        return "Error: Invalid input format"

    # Optional: Validate input length
    if len(input_sequence) != TARGET_LENGTH:
         print(f"Error: Input sequence length is {len(input_sequence)}, expected {TARGET_LENGTH}.")
         return f"Error: Invalid input length"

    # 2. Count the total number of times the integer 0 appears.
    # Example: [5, 8, 2, 0, 6, 0, 2, 6, 0, 1, 4, 0] -> zero_count = 4
    zero_count = count_value(input_sequence, VALUE_TO_COUNT)

    # 3. Calculate the number of ones needed.
    # Example: num_ones = 12 - 4 = 8
    num_ones = TARGET_LENGTH - zero_count

    # 4 & 5. Create a new list with 'zero_count' zeros followed by 'num_ones' ones.
    # Example: [0]*4 + [1]*8 -> [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    output_sequence_list = [OUTPUT_ZERO] * zero_count + [OUTPUT_ONE] * num_ones

    # 6 & 7. Convert the integers in the new list back into strings and join them with spaces.
    # Example: [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1] -> ["0", "0", ..., "1"] -> "0 0 0 0 1 1 1 1 1 1 1 1"
    output_str = SEPARATOR.join(map(str, output_sequence_list))

    # 8. Return the resulting space-separated string.
    return output_str