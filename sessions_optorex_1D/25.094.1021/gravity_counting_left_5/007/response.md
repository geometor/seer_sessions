```python
"""
Transforms an input sequence of integers by first counting the number of non-zero elements (N) 
in the input sequence of length (L). Then, it generates an output sequence of the same 
length (L) consisting of (L - N) zeros followed by N ones.
"""

import numpy as np

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A sequence (list or NumPy array) of integers.

    Returns:
        A NumPy array containing binary integers (0s and 1s)
        representing the transformed sequence.
    """
    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_sequence)

    # Determine the total length (L) of the input sequence.
    total_length = len(input_array)

    # Count the number of non-zero integers (N) within the input sequence.
    # np.count_nonzero is efficient for this.
    non_zero_count = np.count_nonzero(input_array)

    # Calculate the number of zeros required for the output (Z = L - N).
    num_zeros = total_length - non_zero_count

    # Construct the output sequence:
    # Create an array of Z zeros.
    zeros_part = np.zeros(num_zeros, dtype=int)
    # Create an array of N ones.
    ones_part = np.ones(non_zero_count, dtype=int)
    # Concatenate the zero part and the one part.
    output_sequence = np.concatenate((zeros_part, ones_part))

    # Return the constructed output sequence.
    return output_sequence
```