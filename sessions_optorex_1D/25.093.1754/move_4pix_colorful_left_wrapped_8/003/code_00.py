import numpy as np

"""
Transforms a 1D NumPy array of length 12 by splitting it after the 4th element 
(at index 4) and swapping the positions of the resulting two segments.
The first segment contains elements from index 0 to 3.
The second segment contains elements from index 4 to 11.
The output array is formed by concatenating the second segment followed by the first segment.
"""

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Splits the input NumPy array at index 4 and swaps the two segments.

    Args:
        input_array: A 1D NumPy array of shape (12,).

    Returns:
        A 1D NumPy array of shape (12,) with the segments swapped.
    """
    # Define the index at which to split the array (split occurs *before* this index)
    split_index = 4

    # Extract the first segment (elements from index 0 up to split_index)
    first_segment = input_array[:split_index]

    # Extract the second segment (elements from split_index to the end)
    second_segment = input_array[split_index:]

    # Concatenate the second segment followed by the first segment to create the output array
    output_array = np.concatenate((second_segment, first_segment))

    # Return the transformed array
    return output_array