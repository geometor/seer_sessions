import re # Although not strictly needed for this specific solution, it's often useful for string parsing

"""
Transforms an input string containing 12 space-separated integers by moving the first 3 integers to the end of the sequence, preserving relative order within the segments. The output is also a space-separated string.

Example:
Input: "2 8 6 0 0 0 0 0 5 5 4 4"
Output: "0 0 0 0 0 5 5 4 4 2 8 6"
"""

def parse_input_string(input_str: str) -> list[str]:
  """Parses the space-separated string into a list of number strings."""
  # Split the input string by spaces
  elements = input_str.split(' ')
  # Filter out any empty strings that might result from multiple spaces, though
  # the examples suggest single spaces.
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

    # 1. Parse the input string: Split by spaces to get a list of number strings.
    input_list = parse_input_string(input_str)

    # Optional: Add validation if needed, assuming valid 12-element input per examples.
    # if len(input_list) != 12:
    #     raise ValueError("Input string must contain exactly 12 space-separated numbers.")

    # 2. Identify Segments: Slice the list into the first 3 elements and the rest.
    segment1 = input_list[0:3]  # First 3 elements
    segment2 = input_list[3:]   # Elements from index 3 to the end (next 9)

    # 3. Reorder Segments: Concatenate segment2 followed by segment1.
    output_list = segment2 + segment1

    # 4. Format Output String: Join the reordered list elements with spaces.
    output_str = format_output_list(output_list)

    # 5. Return the result.
    return output_str