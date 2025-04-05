import numpy as np

"""
Rearrange a sequence of 12 digits by splitting it into two parts and swapping their order. 
The split occurs after the 4th digit (at index 4). The second part (elements from index 4 onwards) 
comes first in the output, followed by the first part (elements from index 0 to 3).
"""

def transform(input_data):
    """
    Applies the split-and-swap transformation to the input sequence.

    Args:
        input_data: A list or numpy array containing 12 integers.

    Returns:
        A numpy array containing the rearranged sequence of 12 integers.
    """
    # Ensure input is a numpy array for consistent slicing
    input_array = np.array(input_data) 

    # Define the split point (index after the 4th element)
    split_index = 4

    # Check if the input array has the expected length
    if input_array.shape[0] != 12:
        # This case might not be necessary based on problem constraints, 
        # but included for robustness.
        raise ValueError("Input data must contain exactly 12 elements.")

    # Segment 1: First 4 elements (indices 0 to 3)
    segment_1 = input_array[:split_index]

    # Segment 2: Remaining 8 elements (indices 4 to 11)
    segment_2 = input_array[split_index:]

    # Concatenate segment 2 followed by segment 1
    # np.concatenate joins a sequence of arrays along an existing axis
    output_array = np.concatenate((segment_2, segment_1))

    return output_array