```python
import math # Not strictly needed for this task, but included as per template request
import collections # Not strictly needed, but potentially useful for sequence analysis

"""
Transforms a sequence of space-separated single-digit integers.
The transformation identifies the contiguous sub-sequence bounded by the first and last non-zero digits.
This sub-sequence is then reversed in place, while the leading and trailing zeros (if any) remain in their original positions.
If the sequence contains only zeros, it remains unchanged.
"""

def _find_first_non_zero_index(int_list):
  """Finds the index of the first non-zero element."""
  for i, val in enumerate(int_list):
    if val != 0:
      return i
  return -1 # Indicates no non-zero element found

def _find_last_non_zero_index(int_list):
  """Finds the index of the last non-zero element."""
  for i in range(len(int_list) - 1, -1, -1):
    if int_list[i] != 0:
      return i
  return -1 # Indicates no non-zero element found

def transform(input_str: str) -> str:
    """
    Applies the described transformation to the input string sequence.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing the transformed sequence, space-separated.
    """
    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]

    # 2. Find the index of the first non-zero digit.
    start_index = _find_first_non_zero_index(input_list)

    # If no non-zero digit exists, return the original input string.
    if start_index == -1:
      return input_str

    # 3. Find the index of the last non-zero digit.
    # We know at least one non-zero exists if start_index != -1.
    end_index = _find_last_non_zero_index(input_list)

    # 4. Identify the sub-sequence to be reversed.
    # Slice notation [start:end] includes start but excludes end.
    # We want to include the element at end_index, so slice up to end_index + 1.
    sub_sequence_to_reverse = input_list[start_index : end_index + 1]

    # 5. Reverse the identified sub-sequence.
    reversed_sub_sequence = sub_sequence_to_reverse[::-1]

    # 6. Construct the output list.
    # a. Get the leading part (before the first non-zero).
    leading_part = input_list[:start_index]
    # b. Get the trailing part (after the last non-zero).
    trailing_part = input_list[end_index + 1:]

    # Concatenate the parts: leading zeros + reversed non-zero subsequence + trailing zeros
    output_list = leading_part + reversed_sub_sequence + trailing_part

    # 7. Format the output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str

```