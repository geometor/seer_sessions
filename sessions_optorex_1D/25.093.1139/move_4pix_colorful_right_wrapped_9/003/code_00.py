"""
Transforms an input sequence (list or NumPy array) of 12 integers by splitting
it into two parts: the first 8 elements and the last 4 elements. It then
constructs and returns a new sequence (formatted as a space-separated string)
by concatenating the last 4 elements followed by the first 8 elements.
"""

import numpy as np # Import numpy, as the execution environment seems to use it

def format_output_list(output_list: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_sequence) -> str:
    """
    Applies the split-and-swap transformation to the input sequence.

    Args:
        input_sequence: A list or NumPy array containing 12 integers.

    Returns:
        A string representing the rearranged sequence, with elements separated
        by spaces.
    """

    # Ensure input is a list for consistent slicing (handles numpy arrays)
    if isinstance(input_sequence, np.ndarray):
        numbers = input_sequence.tolist()
    else:
        # Assume it's already list-like if not ndarray
        numbers = list(input_sequence) 

    # Define the split point (after the 8th element)
    split_index = 8

    # Check if the input list has the expected length (optional, for robustness)
    # if len(numbers) != 12:
        # Handle error or unexpected input length if necessary
        # Based on the problem description, we assume valid input length
        # pass

    # Split the list into two parts based on the split index
    part1 = numbers[:split_index] # First 8 elements (index 0 to 7)
    part2 = numbers[split_index:] # Last 4 elements (index 8 to 11)

    # Concatenate the parts in the reverse order: part2 then part1
    rearranged_list = part2 + part1

    # Format the rearranged list back into a space-separated string
    output_str = format_output_list(rearranged_list)

    return output_str