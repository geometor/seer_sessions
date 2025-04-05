import numpy as np # Assuming input might be numpy array based on previous error

"""
Take the input sequence of integers, identify the last 3 elements, and move them to the beginning of the sequence, keeping the relative order of both segments (the last 3 and the first n-3).
"""

def transform(input_sequence):
    """
    Transforms the input sequence by cyclically shifting the last 3 elements to the front.

    Args:
        input_sequence: A sequence (e.g., list, tuple, numpy array) of integers.

    Returns:
        A new sequence (type often matches input, e.g., list or numpy array)
        representing the transformed sequence.
    """
    # Determine the length of the input sequence
    n = len(input_sequence)

    # Define the number of elements to move (the split point)
    k = 3 # Based on the examples, we move the last 3 elements

    # Check if the sequence is long enough to perform the split
    # If not, return the sequence unmodified (or handle as appropriate if requirements differ)
    if n < k:
        return input_sequence

    # Identify the last k elements
    # Slicing works similarly for lists, tuples, and numpy arrays
    last_part = input_sequence[n-k:]

    # Identify the first n-k elements
    first_part = input_sequence[:n-k]

    # Construct the output sequence by concatenating the last part followed by the first part
    # Handle numpy array concatenation specifically if input is numpy array
    if isinstance(input_sequence, np.ndarray):
        output_sequence = np.concatenate((last_part, first_part))
    # Otherwise, use standard sequence concatenation (works for lists, tuples)
    else:
         # Convert parts to list first to ensure '+' concatenates, then maybe convert back if needed
         # If input is tuple, output will be tuple. If list, output is list.
        output_sequence = type(input_sequence)(list(last_part) + list(first_part))


    return output_sequence