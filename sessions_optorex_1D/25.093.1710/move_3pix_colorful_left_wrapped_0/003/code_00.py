import math
import numpy as np
import re # Although not strictly needed for this solution, it's often useful for string parsing

"""
Transforms an input sequence of 12 space-separated integers, represented as a single string, by moving the first 3 integers to the end of the sequence. The relative order within the first 3 integers and the remaining 9 integers is preserved.

Example:
Input: "2 8 6 0 0 0 0 0 5 5 4 4"
Output: "0 0 0 0 0 5 5 4 4 2 8 6"

Workflow:
1. Parse the input string into a list of individual number strings.
2. Split the list into two segments: the first 3 elements and the remaining 9 elements.
3. Concatenate the second segment followed by the first segment.
4. Join the elements of the reordered list back into a single space-separated string.
"""

def parse_input_string(input_str: str) -> list[str]:
  """Parses the space-separated string into a list of number strings."""
  # Split the input string by spaces
  elements = input_str.split(' ')
  # Filter out any empty strings that might result from multiple spaces
  return [elem for elem in elements if elem]

def format_output_list(output_list: list[str]) -> str:
  """Formats a list of number strings into a space-separated string."""
  # Join the list elements with a single space
  return " ".join(output_list)

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed sequence of 12 space-separated integers.
    """
    # 1. Parse the input string into a list of number strings
    input_list = parse_input_string(input_str)

    # Basic validation (optional but good practice for robustness)
    if len(input_list) != 12:
       # You might raise an error or handle this case as appropriate
       # For this task, assuming valid input based on examples
       pass 

    # 2. Split the list into two segments
    segment1 = input_list[0:3]  # First 3 elements
    segment2 = input_list[3:]   # Elements from index 3 to the end

    # 3. Concatenate the segments in the new order: segment2 followed by segment1
    output_list = segment2 + segment1

    # 4. Format the resulting list back into a space-separated string
    output_str = format_output_list(output_list)

    return output_str