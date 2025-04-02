"""
Resizes all contiguous horizontal blocks of a specific non-white color within a single-row input grid to match the length of the longest block of that same color found in that row. Resizing is centered around the original block's center. Input and output are 1xN grids.
"""

import numpy as np
from typing import List, Tuple

def find_blocks(sequence: np.ndarray, target_color: int) -> List[Tuple[int, int]]:
    """
    Finds contiguous blocks of a target color in a 1D sequence.

    Args:
        sequence: The 1D numpy array representing the sequence (row).
        target_color: The integer color value to find blocks of.

    Returns:
        A list of tuples, where each tuple is (start_index, end_index)
        of a block.
    """
    blocks = []
    start_index = -1
    n = len(sequence)
    for i, color in enumerate(sequence):
        if color == target_color and start_index == -1:
            # Start of a new block
            start_index = i
        elif color != target_color and start_index != -1:
            # End of the current block (previous index was the end)
            blocks.append((start_index, i - 1))
            start_index = -1
            
    # Check if the sequence ends with a block
    if start_index != -1:
        blocks.append((start_index, n - 1))
        
    return blocks

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid according to the resizing rule.

    Args:
        input_grid: A list containing a single list of integers (representing a 1xN grid).

    Returns:
        A list containing a single list of integers (the transformed 1xN grid).
    """
    
    # Convert input list of lists to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # Validate input shape (must be 1xN)
    if input_array.ndim != 2 or input_array.shape[0] != 1:
        # If input is not a 1xN grid, return it unchanged as per ARC error handling (or raise error)
        # For this specific task structure, returning input seems safest if structure mismatches.
        return input_grid 
        
    # Extract the single row of data
    row_data = input_array[0]
    n = len(row_data) # Width of the grid / length of the row

    # Identify the non-white color (`target_color`)
    target_color = -1
    for color in row_data:
        if color != 0:
            target_color = color
            break
            
    # If no non-white color found, return the input grid as is
    if target_color == -1:
        return input_grid

    # Find all distinct contiguous blocks of the `target_color` in the row
    blocks = find_blocks(row_data, target_color)
    
    # If no blocks found, return the input grid as is
    if not blocks:
        return input_grid
        
    # Calculate the length of each block and determine the maximum length (`max_len`)
    max_len = 0
    for start, end in blocks:
        length = end - start + 1
        if length > max_len:
            max_len = length
            
    # Create a new output row array, initially filled with white (0)
    output_row = np.zeros_like(row_data)

    # For each identified block from the input sequence:
    for start, end in blocks:
        # Calculate the central position (index) of the original block
        # Use floor division for potentially even length blocks
        center = (start + end) // 2 
        
        # Determine the start and end indices for a new block of length `max_len`,
        # centered at the calculated central position.
        # Calculate half-lengths, handling even/odd max_len correctly
        half_len_floor = (max_len - 1) // 2
        half_len_ceil = max_len // 2 # This works because floor + ceil = max_len - 1
        
        new_start = center - half_len_floor
        new_end = center + half_len_ceil # Adjusted calculation for end
        # Note: new_end - new_start + 1 = (center + ceil) - (center - floor) + 1
        # = ceil + floor + 1 = max_len - 1 + 1 = max_len. Correct.

        # Clamp indices to ensure they are within the bounds of the array [0, n-1]
        new_start_clamped = max(0, new_start)
        new_end_clamped = min(n - 1, new_end)
        
        # Fill the corresponding range of indices in the output row array
        # with the `target_color`. Only fill if the range is valid.
        if new_start_clamped <= new_end_clamped:
             output_row[new_start_clamped : new_end_clamped + 1] = target_color

    # Package the completed `output_row` back into the required 1xN grid format (list of lists)
    output_grid = [output_row.tolist()]

    return output_grid