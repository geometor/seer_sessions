"""
Transforms an input sequence (list or NumPy array) of 12 integers by splitting
it into two parts: the first 8 elements and the last 4 elements. It then
constructs and returns a new sequence (formatted as a space-separated string)
by concatenating the last 4 elements followed by the first 8 elements.
"""

import numpy as np # Import numpy as input might be an ndarray

def format_output_list(output_list) -> str:
    """Formats a list/array of items into a space-separated string."""
    # Ensure all elements are strings before joining
    return " ".join(map(str, output_list))

def transform(input_sequence):
    """
    Applies the split-and-swap transformation to the input sequence.

    Args:
        input_sequence: A list or NumPy array containing 12 integers.

    Returns:
        A string representing the rearranged sequence, with elements separated
        by spaces.
    """
    # Ensure input is treated as a list or sequence compatible with slicing
    # No explicit conversion needed if slicing works directly on input type
    numbers = input_sequence

    # Define the split point (after the 8th element)
    split_index = 8

    # Split the sequence into two parts using slicing
    # Part 1 contains elements from index 0 up to (but not including) split_index
    part1 = numbers[:split_index]
    # Part 2 contains elements from split_index to the end
    part2 = numbers[split_index:]

    # Concatenate the parts in the reverse order: part2 then part1
    # This works for lists and numpy arrays (though array concatenation might differ)
    # If input is guaranteed list or converted, simple list concatenation is fine.
    # If input could be np.array, np.concatenate might be safer, but + often works element-wise
    # Let's assume list concatenation is intended based on the logic. If input is np.array,
    # slicing might return views or copies, but list conversion ensures consistency.
    # Using list() ensures we are dealing with lists for concatenation.
    rearranged_list = list(part2) + list(part1)

    # Format the rearranged list back into a space-separated string
    output_str = format_output_list(rearranged_list)

    return output_str