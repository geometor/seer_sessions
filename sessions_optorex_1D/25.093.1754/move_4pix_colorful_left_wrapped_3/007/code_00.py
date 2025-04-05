import numpy as np

"""
Rearrange a sequence of 12 integers by splitting it into two parts after the 
4th element (at index 4) and swapping the order of these two parts. The output 
is the concatenation of the second part (elements from index 4 to 11) followed 
by the first part (elements from index 0 to 3).
"""

def transform(input_sequence):
    """
    Applies the split-and-swap transformation to the input sequence.

    Args:
        input_sequence: A list or numpy array containing 12 integers.

    Returns:
        A numpy array containing the rearranged sequence of 12 integers.
    """

    # Ensure the input is a NumPy array for consistent slicing and concatenation
    input_array = np.array(input_sequence)

    # Define the index where the split occurs (after the 4th element)
    split_index = 4

    # --- Optional: Check for expected length (based on problem description) ---
    # if input_array.shape[0] != 12:
    #     raise ValueError("Input sequence must contain exactly 12 elements.")
    # --- End Optional Check ---

    # Identify the first segment: elements from index 0 up to (not including) split_index
    # Example: For [6, 9, 5, 0, 0, 0, 0, 0, 0, 1, 8, 6], segment_1 is [6, 9, 5, 0]
    segment_1 = input_array[:split_index]

    # Identify the second segment: elements from split_index to the end
    # Example: For [6, 9, 5, 0, 0, 0, 0, 0, 0, 1, 8, 6], segment_2 is [0, 0, 0, 0, 0, 1, 8, 6]
    segment_2 = input_array[split_index:]

    # Construct the output sequence by concatenating segment 2 followed by segment 1
    # Example: Concatenate [0, 0, 0, 0, 0, 1, 8, 6] and [6, 9, 5, 0]
    # Result: [0, 0, 0, 0, 0, 1, 8, 6, 6, 9, 5, 0]
    output_array = np.concatenate((segment_2, segment_1))

    # Return the rearranged array
    return output_array