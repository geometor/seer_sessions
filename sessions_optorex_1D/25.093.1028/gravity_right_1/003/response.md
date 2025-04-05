```python
import numpy as np
import math # math is available but not used in this specific transformation

"""
Moves all zero digits to the beginning of the sequence while preserving the relative order of the non-zero digits.
"""

def partition_sequence(sequence):
    """
    Helper function to separate a sequence into zero and non-zero elements.

    Args:
        sequence: An iterable (list or array) of numbers.

    Returns:
        A tuple containing two lists: (list_of_zeros, list_of_non_zeros).
        The relative order of elements within list_of_non_zeros is preserved.
    """
    zeros = []
    non_zeros = []
    # Iterate through the input sequence
    for item in sequence:
        # Check if the element is zero
        if item == 0:
            zeros.append(item)
        else:
            # If not zero, add to the non_zeros list
            non_zeros.append(item)
    return zeros, non_zeros

def transform(input_sequence):
    """
    Transforms an input sequence (list or NumPy array) of integers by moving
    all zeros to the front while maintaining the relative order of non-zero digits.

    Args:
        input_sequence: A list or NumPy array containing single-digit integers.
                        Example: [9, 0, 0, 0, 9, 0, 0, 7, 6, 0, 6, 0]

    Returns:
        A new list containing the transformed sequence of integers.
        Example: [0, 0, 0, 0, 0, 0, 0, 9, 9, 7, 6, 6]
    """

    # Ensure input is iterable (convert NumPy array to list if necessary,
    # otherwise assume it's list-like)
    if isinstance(input_sequence, np.ndarray):
        # Convert numpy array to list for consistent processing
        work_sequence = input_sequence.tolist()
    else:
        # Assume it's already a list or compatible iterable
        work_sequence = list(input_sequence)

    # Separate the sequence into zeros and non-zeros using the helper function
    zeros, non_zeros = partition_sequence(work_sequence)

    # Construct the output sequence by concatenating the lists: zeros first, then non-zeros
    output_sequence = zeros + non_zeros

    # Return the resulting transformed list
    return output_sequence
```