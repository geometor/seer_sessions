import math # Although not strictly needed for this logic, included as per instruction
import numpy as np # Useful for counting non-zeros efficiently

"""
Transforms an input string of 12 space-separated digits (0-9) into an output string of 12 space-separated binary digits (0 or 1). The number of '1's at the beginning of the output sequence equals the count of non-zero digits in the input sequence. The remaining positions in the output sequence are filled with '0's to maintain a total length of 12.
"""

def count_non_zeros(numbers):
  """Counts the number of non-zero elements in a list of numbers."""
  # Using numpy's count_nonzero is efficient for numerical lists
  # Convert to numpy array first if it's a standard list
  return np.count_nonzero(np.array(numbers))
  # Alternative without numpy:
  # count = 0
  # for num in numbers:
  #   if num != 0:
  #     count += 1
  # return count

def transform(input_str):
    """
    Applies the transformation rule to the input string.

    Args:
      input_str: A string containing 12 space-separated digits (e.g., "4 0 0 3 3 2 9 7 7 0 0 0").

    Returns:
      A string containing 12 space-separated binary digits (e.g., "1 1 1 1 1 1 1 0 0 0 0 0").
    """

    # 1. Accept the input as a single string containing 12 space-separated digits.
    # 2. Split the input string by spaces to get a list of digit strings.
    # 3. Convert each digit string in the list to an integer, creating a list of 12 integers.
    input_numbers = [int(digit) for digit in input_str.split()]

    # 4. Initialize a counter `non_zero_count` to 0.
    # 5. Iterate through the list of integers. For each integer, if it is not 0, increment `non_zero_count`.
    #    (Using helper function)
    non_zero_count = count_non_zeros(input_numbers)

    # 6. Create an empty list called `output_list`.
    output_list = []

    # 7. Append the integer `1` to `output_list` exactly `non_zero_count` times.
    for _ in range(non_zero_count):
        output_list.append(1)

    # 8. Calculate the number of zeros needed: `zero_count = 12 - non_zero_count`.
    #    (Assuming input length is always 12 based on examples)
    total_length = 12 # Or use len(input_numbers) for more generality
    zero_count = total_length - non_zero_count

    # 9. Append the integer `0` to `output_list` exactly `zero_count` times.
    for _ in range(zero_count):
        output_list.append(0)

    # 10. Convert each integer in `output_list` back into a string.
    output_str_list = [str(num) for num in output_list]

    # 11. Join the strings in `output_list` together using a single space as a separator.
    output_str = " ".join(output_str_list)

    # 12. Return the resulting string.
    return output_str
