import math

"""
Identifies the repeating base pattern in the initial non-zero segment of the input sequence (which is assumed to be two repetitions of the pattern) and uses this pattern to replace the trailing zeros, extending the sequence to the original input length.
"""

def parse_input(input_str: str) -> list[int]:
  """Converts a space-separated string of digits into a list of integers."""
  return [int(x) for x in input_str.strip().split()]

def format_output(output_list: list[int]) -> str:
  """Converts a list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string representing the input sequence of space-separated digits.

    Returns:
        A string representing the transformed output sequence.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)
    total_length = len(input_list)

    # Find the end of the non-zero segment
    non_zero_end_index = total_length
    for i, num in enumerate(input_list):
        if num == 0:
            non_zero_end_index = i
            break
    
    # Extract the non-zero segment
    non_zero_segment = input_list[:non_zero_end_index]

    # Determine the base pattern (first half of the non-zero segment)
    # Based on the observation that the non-zero part is always two repetitions
    pattern_length = len(non_zero_segment) // 2
    base_pattern = non_zero_segment[:pattern_length]
    
    # Initialize the output list with the non-zero segment
    output_list = list(non_zero_segment) # Create a copy

    # Fill the remaining part of the output list by repeating the base pattern
    pattern_index = 0
    while len(output_list) < total_length:
        output_list.append(base_pattern[pattern_index])
        pattern_index = (pattern_index + 1) % pattern_length # Cycle through the pattern

    # Format the output list back into a string
    return format_output(output_list)

# Example Usage (optional, for testing)
# print(transform("9 7 9 7 0 0 0 0 0 0 0 0"))
# print(transform("3 5 5 8 3 5 5 8 0 0 0 0"))
# print(transform("1 5 1 8 4 1 5 1 8 4 0 0"))