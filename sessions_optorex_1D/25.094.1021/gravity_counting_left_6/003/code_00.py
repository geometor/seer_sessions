import numpy as np
import collections # Although not strictly necessary for this specific solution, it's good practice.

"""
Transforms an input NumPy array of 12 integers.
Counts the total number of zeros (N) in the input array.
Generates an output sequence as a space-separated string,
consisting of N zeros followed by (12-N) ones.
"""

def count_value(data, value_to_count):
  """Counts occurrences of a specific value in a list or NumPy array."""
  if isinstance(data, np.ndarray):
    # Efficiently count using NumPy for arrays
    return np.count_nonzero(data == value_to_count)
  elif isinstance(data, list):
    # Use list's count method
    return data.count(value_to_count)
  else:
    # Fallback for other iterables, less efficient
    count = 0
    for item in data:
      if item == value_to_count:
        count += 1
    return count

def transform(input_array: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_array: A NumPy array containing 12 integers (0-9).

    Returns:
        A string containing 12 space-separated integers (0 or 1),
        representing the transformed sequence.
    """

    # Define constants for clarity
    TARGET_LENGTH = 12
    VALUE_TO_COUNT = 0
    OUTPUT_ZERO = 0
    OUTPUT_ONE = 1

    # Ensure input has the expected length (optional but good practice)
    if input_array.size != TARGET_LENGTH:
        # Handle error appropriately, e.g., raise ValueError or return an error indicator
        # For this task, we assume valid input based on examples.
        pass 

    # Count the occurrences of the integer 0 in the input array
    # Using a helper function for clarity
    zero_count = count_value(input_array, VALUE_TO_COUNT)
    # Alternatively, directly:
    # zero_count = np.count_nonzero(input_array == 0)
    # Or converting to list first (less efficient for large arrays):
    # zero_count = input_array.tolist().count(0)

    # Calculate the number of ones required for the output
    num_ones = TARGET_LENGTH - zero_count

    # Construct the output sequence as a list
    # Create a list containing 'zero_count' zeros
    output_zeros = [OUTPUT_ZERO] * zero_count
    # Create a list containing 'num_ones' ones
    output_ones = [OUTPUT_ONE] * num_ones
    # Combine the two lists to form the final output sequence
    output_sequence_list = output_zeros + output_ones

    # Convert the output sequence (list of integers) back to a space-separated string
    # Example: [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1] -> "0 0 0 0 1 1 1 1 1 1 1 1"
    output_str = " ".join(map(str, output_sequence_list))

    return output_str