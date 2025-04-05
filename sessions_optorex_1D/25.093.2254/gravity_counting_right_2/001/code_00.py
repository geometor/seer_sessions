import math
import collections

"""
Counts the number of non-zero digits in the input sequence and generates an output sequence of the same length (12). The output sequence starts with a number of '1's equal to the count of non-zero digits, followed by '0's to fill the remaining positions.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated input string into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def count_non_zeros(numbers: list[int]) -> int:
    """Counts the number of non-zero elements in a list of integers."""
    count = 0
    for num in numbers:
        if num != 0:
            count += 1
    return count

def format_output(output_list: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Transforms the input sequence according to the described rule.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing 12 space-separated binary digits ('1' or '0').
    """
    # Parse the input string into a list of numbers
    input_numbers = parse_input(input_str)

    # Count the non-zero numbers in the input list
    non_zero_count = count_non_zeros(input_numbers)

    # Determine the total length (should always be 12 based on examples)
    total_length = len(input_numbers) # Or simply use 12

    # Construct the output list
    # Start with 'non_zero_count' number of 1s
    output_list = [1] * non_zero_count
    # Append the required number of 0s to reach the total length
    output_list.extend([0] * (total_length - non_zero_count))

    # Format the output list into a space-separated string
    output_str = format_output(output_list)

    return output_str
