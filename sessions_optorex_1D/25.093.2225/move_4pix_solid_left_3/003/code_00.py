import numpy as np

"""
Receive the input sequence (which is a list or array of 12 integers). Take a slice of the input sequence starting from the 5th element (index 4) through the end. Create a new sequence containing 4 elements, each with the value 0. Concatenate the slice and the new sequence to form the output sequence. Return the output sequence.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the elements of a 1D numpy array 4 positions to the left,
    padding the right end with zeros.

    Args:
        input_grid: A 1D numpy array of integers.

    Returns:
        A new 1D numpy array representing the transformed sequence.
    """

    # Define the amount to shift left
    shift_amount = 4

    # Define the value used for padding
    pad_value = 0

    # Ensure input is a numpy array (it should be based on prior errors)
    if not isinstance(input_grid, np.ndarray):
        # This case might not be strictly necessary if the environment guarantees ndarray
        input_grid = np.array(input_grid)

    # --- Transformation Steps ---

    # 1. Take a slice of the input sequence starting from the shift_amount index.
    #    This effectively removes the first 'shift_amount' elements.
    #    Example: if input is [0,0,0,0,2,2,2,2,2,2,2,0] and shift is 4,
    #    this slice will be [2,2,2,2,2,2,2,0]
    shifted_part = input_grid[shift_amount:]

    # 2. Create a new sequence (padding) containing 'shift_amount' elements,
    #    each with the value 'pad_value'.
    #    Example: if shift is 4 and pad_value is 0, this creates [0,0,0,0]
    #    Using the same dtype as the input prevents potential type issues.
    padding_part = np.full(shift_amount, pad_value, dtype=input_grid.dtype)

    # 3. Concatenate the slice from step 1 and the padding sequence from step 2.
    #    Example: Concatenating [2,2,2,2,2,2,2,0] and [0,0,0,0] gives
    #    [2,2,2,2,2,2,2,0,0,0,0,0]
    output_grid = np.concatenate((shifted_part, padding_part))

    # 4. Return the resulting sequence.
    return output_grid