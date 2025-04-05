"""
Transforms an input sequence of 12 digits (provided as a list or NumPy array) by moving the last 4 digits to the beginning of the sequence, followed by the first 8 digits. The output is formatted as a space-separated string.
"""

import numpy as np
import math #虽然目前不一定需要，但根据模板和习惯性导入

# Helper function to split the sequence using slicing
def slice_sequence(sequence, split_point):
    """Splits a sequence (list or array) at a given index."""
    # Note: Slicing works similarly for lists and NumPy arrays
    return sequence[:split_point], sequence[split_point:]

# Helper function to concatenate sequences
def concatenate_sequences(seq1, seq2):
    """Concatenates two sequences (handles lists or NumPy arrays)."""
    # Using list concatenation as it's straightforward and handles both types if converted
    # If inputs are guaranteed NumPy arrays, np.concatenate is more idiomatic
    # For mixed or list inputs, list concatenation is simpler.
    return list(seq1) + list(seq2) # Convert to list to ensure compatibility

# Helper function to format the sequence back to a string
def format_sequence_to_string(sequence):
    """Joins a list of items into a space-separated string after converting items to string."""
    return " ".join(map(str, sequence))

def transform(input_sequence) -> str:
    """
    Applies the transformation rule: moves the last 4 elements to the front.

    Args:
        input_sequence: A list or NumPy array containing 12 digits (or items representable as strings).

    Returns:
        A string containing the transformed sequence of 12 elements, space-separated.
    """
    # Assuming input_sequence is a list or NumPy array of length 12
    # No need for input_str.split(' ') anymore as input is not a string

    # Validate input length (optional but good practice)
    if len(input_sequence) != 12:
        raise ValueError("Input sequence must contain exactly 12 elements.")

    # Define the split point
    split_point = 8

    # 1. Identify the first 8 elements as the "first segment".
    # 2. Identify the last 4 elements as the "second segment".
    # Using the slice_sequence helper function
    first_segment, second_segment = slice_sequence(input_sequence, split_point)

    # 3. Construct the output sequence by placing the "second segment" first,
    #    followed immediately by the "first segment".
    # Using the concatenate_sequences helper function
    # Ensure segments are treated correctly (e.g., as lists for concatenation)
    output_sequence_list = concatenate_sequences(second_segment, first_segment)

    # 4. Format the resulting sequence as a string with elements separated by spaces.
    # Using the format_sequence_to_string helper function
    output_str = format_sequence_to_string(output_sequence_list)

    return output_str