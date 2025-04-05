```python
import re

"""
Parses an input string of 12 space-separated numbers, splits it into two segments 
(the first 4 numbers and the last 8 numbers), and swaps their positions to form 
the output string.
"""

def parse_input(input_str: str) -> list[str]:
    """Parses the space-separated input string into a list of strings."""
    return input_str.split(' ')

def split_sequence(data: list[str], split_index: int) -> tuple[list[str], list[str]]:
    """Splits the sequence at the given index."""
    segment1 = data[:split_index]
    segment2 = data[split_index:]
    return segment1, segment2

def format_output(data: list[str]) -> str:
    """Formats the list of strings into a space-separated output string."""
    return ' '.join(data)

def transform(input_str: str) -> str:
    """
    Transforms the input string by splitting it after the 4th element
    and swapping the resulting two segments.

    Args:
        input_str: A string containing 12 space-separated numbers.

    Returns:
        A string containing the transformed sequence of 12 space-separated numbers.
    """
    # Parse the input string into a list of number strings.
    numbers = parse_input(input_str)

    # Define the split point (after the 4th element, which is index 4).
    split_point = 4

    # Split the list into two segments.
    first_segment, second_segment = split_sequence(numbers, split_point)

    # Create the output list by concatenating the second segment followed by the first segment.
    output_list = second_segment + first_segment

    # Join the elements of the output list with spaces to form the final output string.
    output_str = format_output(output_list)

    return output_str

```