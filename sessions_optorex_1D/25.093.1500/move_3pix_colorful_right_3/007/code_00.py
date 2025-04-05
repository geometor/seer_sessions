import numpy as np
import math # although not strictly needed for this specific task, good practice

"""
Right-shift a sequence of integers, provided as a NumPy array, by a fixed amount (3), 
padding the start with zeros. The result is returned as a list of integers.

1. Receive the input sequence as a NumPy array.
2. Convert the input NumPy array (specifically, its first row if it's 2D, or the array itself if 1D) into a standard Python list of integers.
3. Define the shift amount as 3.
4. Define the padding value as 0.
5. Get the length (N) of the integer list.
6. Create a new output list of length N, initialized entirely with the padding value (0).
7. Iterate through the input list indices `i` from 0 up to (but not including) `N - shift_amount`.
8. For each index `i`, copy the value from the input list at index `i` to the output list at index `i + shift_amount`.
9. Return the completed output list containing the shifted sequence of integers.
"""

def _perform_right_shift(sequence: list[int], amount: int, padding_value: int = 0) -> list[int]:
    """
    Shifts the elements of a list to the right by a specified amount, 
    padding the beginning with a given value.
    
    Args:
        sequence: The input list of integers.
        amount: The number of positions to shift right.
        padding_value: The value to use for padding at the start.

    Returns:
        A new list containing the shifted and padded sequence.
    """
    n = len(sequence)
    # Initialize the output sequence with the padding value
    output_sequence = [padding_value] * n
    
    # Determine the number of elements to copy
    # Ensure we don't try to read past the end of the input or write past the end of the output
    elements_to_copy = max(0, n - amount) 
    
    # Copy elements from the input to the shifted positions in the output
    for i in range(elements_to_copy):
        # The element at input index i moves to output index i + amount
        if i + amount < n: # Check bounds for safety, though loop range should handle it
            output_sequence[i + amount] = sequence[i]
            
    return output_sequence

def transform(input_grid: np.ndarray) -> list[int]:
    """
    Applies the right-shift transformation to the input NumPy array sequence.
    """
    # Define the fixed shift amount and padding value
    shift_amount = 3
    padding_value = 0

    # Convert the input NumPy array to a Python list.
    # Handle potential 2D array (shape 1xN) or 1D array (shape N,)
    if input_grid.ndim > 1 and input_grid.shape[0] == 1:
        # If it's 2D with one row, extract that row
        input_list = input_grid[0].tolist()
    elif input_grid.ndim == 1:
        # If it's already 1D, convert directly
        input_list = input_grid.tolist()
    else:
        # Handle unexpected shapes, perhaps raise an error or return empty
        # For now, assume valid input based on examples and return empty for invalid.
        # Or default to the first row if multiple rows exist, although examples don't show this.
        # Let's try extracting the first row if ndim > 1, regardless of row count, 
        # as a fallback, though this might be incorrect for other tasks.
        # A safer default might be to raise ValueError('Input grid has unexpected shape.')
        # Sticking to the most likely case based on examples:
        if input_grid.shape[0] > 0:
             input_list = input_grid[0].tolist() # Assume first row is the target
        else:
             input_list = [] # Handle empty array case


    # Perform the right shift operation using the helper function
    output_list = _perform_right_shift(input_list, shift_amount, padding_value)

    # Return the resulting list of integers
    return output_list