```python
"""
Transforms an input sequence (expected as a NumPy array or list of integers) by moving the first 3 elements to the end of the sequence, preserving the relative order of both the moved elements and the remaining elements. This is equivalent to a left rotation by 3 positions.
"""

import numpy as np

def transform(input_sequence):
    """
    Moves the first 3 elements of the input sequence to the end.

    Args:
        input_sequence: A NumPy array or list containing the sequence of integers.

    Returns:
        A NumPy array containing the transformed sequence.
    """
    # Convert input to NumPy array if it's not already, ensuring compatibility
    input_array = np.array(input_sequence)

    # Define the number of elements to move from the start to the end
    n_to_move = 3

    # Handle cases where the array might be shorter than n_to_move, although examples suggest length >= 3
    if len(input_array) <= n_to_move:
        # If the array is too short, moving the first 'n' elements doesn't change the order
        # or isn't well-defined by the examples. Returning the original array is a safe default.
        return input_array

    # Slice the array into two parts:
    # head_segment: The first n_to_move elements
    head_segment = input_array[:n_to_move]
    # tail_segment: The remaining elements from index n_to_move onwards
    tail_segment = input_array[n_to_move:]

    # Concatenate the tail_segment followed by the head_segment to form the output sequence
    output_sequence = np.concatenate((tail_segment, head_segment))

    # Return the transformed sequence as a NumPy array
    return output_sequence

```