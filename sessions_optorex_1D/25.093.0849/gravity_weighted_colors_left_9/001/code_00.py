import collections

"""
1. Parse the input string into a sequence of individual digit numbers.
2. Sort this sequence of digits in non-decreasing (ascending) numerical order.
3. Format the sorted sequence back into a string with digits separated by spaces.
4. Return the formatted string as the output.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output(numbers: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, numbers))

def transform(input_str: str) -> str:
    """
    Takes a string of space-separated digits, sorts them numerically
    in non-decreasing order, and returns the sorted sequence as a
    space-separated string.
    """
    # 1. Parse the input string into a sequence of individual digit numbers.
    numbers = parse_input(input_str)

    # 2. Sort this sequence of digits in non-decreasing (ascending) numerical order.
    # Python's sort is stable and sorts in ascending order by default.
    sorted_numbers = sorted(numbers)

    # 3. Format the sorted sequence back into a string with digits separated by spaces.
    output_str = format_output(sorted_numbers)

    # 4. Return the formatted string as the output.
    return output_str
