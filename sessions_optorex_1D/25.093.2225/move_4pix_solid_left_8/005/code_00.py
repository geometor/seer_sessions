import numpy as np
from typing import Tuple, Optional

"""
Identifies the contiguous block of identical non-zero digits in the 1D input sequence 
(length 12). Creates a new sequence of 12 zeros. Shifts the identified block 4 
positions to the left and places it into the new sequence at the calculated position. 
Returns the resulting sequence.
"""

def find_block_in_sequence(sequence: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous block of identical non-zero digits in a 1D numpy array.

    Args:
        sequence: The 1D input numpy array of digits.

    Returns:
        A tuple containing (start_index, end_index, value) of the block,
        or None if no such block is found or if the block rule is violated.
    """
    start_index = -1
    block_value = -1
    n = sequence.size

    for i in range(n):
        digit = sequence[i] # Access element directly
        if digit != 0:
            # Found a non-zero digit
            if start_index == -1:
                # This is the start of a potential block
                start_index = i
                block_value = digit
            elif digit != block_value:
                # Found a different non-zero digit, violates the rule of identical digits
                # Or could indicate a second block, also violating the rule.
                # Based on problem description, this shouldn't happen.
                return None # Indicate error or unexpected format
        elif start_index != -1:
            # Found a zero after a block started. The block ended at the previous index.
            return start_index, i - 1, block_value
            
    # If the loop finishes and a block was started, it means the block extends to the end.
    if start_index != -1:
        return start_index, n - 1, block_value
        
    # If the loop finishes and no block was started, return None.
    return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the rule: find the non-zero block 
    and shift it 4 positions to the left.
    """
    # Ensure input is treated as a 1D sequence
    # The ARC framework typically provides numpy arrays. Flatten ensures 1D.
    input_sequence = input_grid.flatten()
    n = input_sequence.size 
    
    # Basic validation - Check if length is 12 as expected from examples
    if n != 12:
        # Handle unexpected input size if necessary, here just proceeding
        pass 

    # Initialize output_grid as a 1D array of zeros with the same length
    output_grid = np.zeros(n, dtype=int)

    # Find the contiguous block of non-zero identical digits
    block_info = find_block_in_sequence(input_sequence)

    # If a valid block was found
    if block_info:
        start_index, end_index, block_value = block_info

        # Calculate the new start and end indices by shifting left by 4
        new_start_index = start_index - 4
        new_end_index = end_index - 4

        # Check if the new indices are within the valid bounds [0, n-1]
        # Note: Slicing handles the upper bound correctly, mainly check start index
        # and ensure the slice doesn't try to write out of bounds negativity
        if new_start_index >= 0 and new_end_index < n :
             # Fill the output grid with the block value at the new position
             # Use numpy slicing for efficiency
             output_grid[new_start_index : new_end_index + 1] = block_value
        # else:
            # Optional: Handle cases where shift goes out of bounds, though
            # examples suggest this won't happen or isn't required.
            # print(f"Warning: Shift results in out-of-bounds indices: {new_start_index}-{new_end_index}")
            pass

    # Reshape the output to match the original input grid's shape if it wasn't 1D
    # If input was guaranteed 1D or 1xN, this might not be strictly necessary,
    # but it's safer. Check original shape.
    # For this specific task description (1D sequences), reshaping might not be needed, 
    # but let's keep it flexible. If input_grid is already 1D, reshape does nothing harmful.
    try:
        output_grid = output_grid.reshape(input_grid.shape)
    except ValueError:
        # This might happen if n != input_grid.size, indicating an issue earlier.
        # For this task, size should always be 12.
        # Fallback to returning the 1D array if reshape fails.
        pass

    return output_grid