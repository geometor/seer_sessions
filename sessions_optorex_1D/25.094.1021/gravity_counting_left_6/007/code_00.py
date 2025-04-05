import numpy as np

"""
Transforms an input NumPy array of 12 integers.
Counts the total number of zeros (N) in the input array.
Generates an output sequence as a space-separated string,
consisting of N zeros followed by (12-N) ones.
"""

def count_value_in_array(data_array: np.ndarray, value_to_count) -> int:
  """Counts occurrences of a specific value in a NumPy array."""
  return np.count_nonzero(data_array == value_to_count)

def transform(input_array: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_array: A NumPy array containing 12 integers (0-9).

    Returns:
        A string containing 12 space-separated integers (0 or 1),
        representing the transformed sequence.
    """

    # Define constants for clarity and maintainability
    TARGET_LENGTH = 12
    VALUE_TO_COUNT = 0
    OUTPUT_ZERO = 0
    OUTPUT_ONE = 1
    SEPARATOR = " "

    # 1. Ensure input is a NumPy array (optional, depends on environment guarantees)
    #    If not already an array, convert it: input_array = np.array(input_data)

    # 2. Validate input array size (optional but good practice)
    if input_array.size != TARGET_LENGTH:
         # Handle error: raise ValueError, return specific error string, etc.
         # Assuming valid input size based on problem description.
         print(f"Warning: Input array size is {input_array.size}, expected {TARGET_LENGTH}.")
         # Adjust TARGET_LENGTH if we need to handle variable lengths, but problem implies fixed length.
         # target_length = input_array.size # Alternative if length can vary

    # 3. Count how many times the integer 0 appears in the input array.
    #    Use a helper function for clarity.
    zero_count = count_value_in_array(input_array, VALUE_TO_COUNT)
    #    Directly: zero_count = np.count_nonzero(input_array == 0)

    # 4. Calculate the number of ones required for the output sequence.
    num_ones = TARGET_LENGTH - zero_count

    # 5. Create a list containing 'zero_count' zeros.
    output_zeros = [OUTPUT_ZERO] * zero_count

    # 6. Create a list containing 'num_ones' ones.
    output_ones = [OUTPUT_ONE] * num_ones

    # 7. Concatenate the lists to form the final sequence list.
    output_sequence_list = output_zeros + output_ones

    # 8. Convert each integer in the final list to its string representation.
    output_string_list = [str(num) for num in output_sequence_list]
    #    Alternatively using map: output_string_list = list(map(str, output_sequence_list))

    # 9. Join the resulting strings with a single space delimiter.
    output_str = SEPARATOR.join(output_string_list)

    # 10. Return the resulting space-separated string.
    return output_str