import re

"""
Rearrange a sequence of 12 integers by swapping two fixed-length blocks.
The input sequence is split after the 4th integer. The output sequence is
formed by concatenating the second block (integers 5 through 12) followed
by the first block (integers 1 through 4).
"""

def transform(input_str: str) -> str:
    """
    Rearranges a space-separated string of 12 integers.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the rearranged 12 space-separated integers.
    """
    # Parse the input string into a list of integers.
    # Use regular expression to find all sequences of digits, handling potential multiple spaces.
    numbers = [int(x) for x in re.findall(r'\d+', input_str)]

    # Ensure the input has exactly 12 numbers
    if len(numbers) != 12:
        raise ValueError("Input string must contain exactly 12 integers.")

    # Split the list into two parts.
    # Part 1: first 4 integers (indices 0 to 3)
    part1 = numbers[0:4]
    # Part 2: remaining 8 integers (indices 4 to 11)
    part2 = numbers[4:12]

    # Concatenate part2 followed by part1.
    output_numbers = part2 + part1

    # Convert the resulting list of integers back into a space-separated string.
    output_str = " ".join(map(str, output_numbers))

    return output_str
