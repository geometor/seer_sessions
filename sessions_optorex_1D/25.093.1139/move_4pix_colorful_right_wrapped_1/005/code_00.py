"""
Transforms an input sequence of 12 space-separated digits by moving the last 4 digits to the beginning of the sequence, followed by the first 8 digits.
"""

import numpy as np # Standard import, though not strictly necessary for this task
import math # Standard import, though not strictly necessary for this task

# Helper function to parse the input string into a list
def parse_input_string(input_str: str) -> list:
    """Splits the input string by spaces into a list of strings."""
    return input_str.split(' ')

# Helper function to slice the sequence into two segments
def split_sequence_segments(sequence: list, split_point: int) -> tuple:
    """Splits a list into two parts at the given index."""
    first_segment = sequence[:split_point]
    second_segment = sequence[split_point:]
    return first_segment, second_segment

# Helper function to combine the segments in the new order
def combine_segments(segment1: list, segment2: list) -> list:
    """Concatenates segment2 followed by segment1."""
    # Note: The order is specific to the task requirement
    return segment2 + segment1

# Helper function to format the list back into an output string
def format_output_string(sequence: list) -> str:
    """Joins the elements of a list into a space-separated string."""
    return " ".join(sequence)

def transform(input_str: str) -> str:
    """
    Applies the transformation rule: moves the last 4 digits to the front,
    followed by the first 8 digits.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed sequence of 12 space-separated digits.
    """

    # 1. Parse the input string into a list of digit strings
    parsed_input_sequence = parse_input_string(input_str)

    # Optional: Validate length (though previous analysis confirmed inputs are always 12)
    # if len(parsed_input_sequence) != 12:
    #     raise ValueError("Input sequence must contain exactly 12 digits.")

    # 2. Define the split point
    split_index = 8

    # 3. Identify the first 8 elements (first segment) and last 4 elements (second segment)
    first_segment, second_segment = split_sequence_segments(parsed_input_sequence, split_index)

    # 4. Construct the new sequence by concatenating the second segment followed by the first segment
    reordered_sequence = combine_segments(first_segment, second_segment)

    # 5. Format the new sequence back into a space-separated string
    output_str = format_output_string(reordered_sequence)

    # Return the final string
    return output_str