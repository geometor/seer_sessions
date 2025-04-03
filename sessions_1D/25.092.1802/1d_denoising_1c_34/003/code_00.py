"""
Identify the single largest contiguous horizontal block of the non-background color 
within the input grid's single row. Create an output grid of the same dimensions 
containing only this block at the same position, with all other pixels set to the 
background color (white/0). Assumes input grid has exactly one row.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_horizontal_blocks(row: np.ndarray, target_color: int) -> List[Tuple[int, int, int]]:
    """
    Finds all contiguous horizontal blocks of a target color in a 1D array (row).

    Args:
        row: The 1D numpy array representing the row.
        target_color: The integer color value to search for.

    Returns:
        A list of tuples, where each tuple represents a block:
        (start_column, end_column_inclusive, length). 
        Returns an empty list if no blocks are found.
    """
    blocks = []
    in_block = False
    start_col = -1
    
    for col_idx, pixel in enumerate(row):
        # Start of a new block
        if pixel == target_color and not in_block:
            in_block = True
            start_col = col_idx
            
        # End of the current block (found a different color or end of row)
        # Note: The end condition must also trigger if we are in a block at the *last* pixel
        is_last_pixel = (col_idx == len(row) - 1)
        ends_block = (pixel != target_color and in_block) or (is_last_pixel and in_block)
        
        if ends_block:
            in_block = False
            # Determine the correct end index (inclusive)
            end_col_inclusive = col_idx - 1 if pixel != target_color else col_idx
            length = end_col_inclusive - start_col + 1
            blocks.append((start_col, end_col_inclusive, length))
            start_col = -1 # Reset start index

    return blocks

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by keeping only the largest horizontal block 
    of the primary non-white color.

    Args:
        input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed output grid (1xN).
    """
    # Convert input to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # Basic validation for expected 1-row structure
    if input_array.shape[0] != 1:
        # Handle unexpected input shape, perhaps return input or raise error
        # For ARC, constraints likely guarantee 1xN, but good practice
        print(f"Warning: Expected input with 1 row, got {input_array.shape[0]}. Processing first row only.")
        # Or return input_grid # Depending on desired error handling
    
    # Extract the single active row
    active_row = input_array[0, :]
    height, width = input_array.shape

    # Initialize the output grid with the background color (0)
    output_array = np.zeros_like(input_array)

    # Identify the primary non-white color
    unique_colors = np.unique(active_row)
    primary_color = 0
    for color in unique_colors:
        if color != 0:
            primary_color = color
            break # Assume only one non-white color as per examples

    # If no primary color found (input is all background), return the zeroed output
    if primary_color == 0:
        return output_array.tolist()

    # Find all contiguous horizontal blocks of the primary color in the active row
    blocks = find_horizontal_blocks(active_row, primary_color)

    # If no blocks were found, return the zeroed output
    if not blocks:
        return output_array.tolist()

    # Find the largest block based on length (item[2])
    # If there's a tie, max() naturally selects the first one encountered
    largest_block = max(blocks, key=lambda item: item[2])
    
    # Extract details of the largest block
    start_col, end_col_inclusive, _ = largest_block

    # Populate the output grid's row with the largest block
    # Numpy slicing is [start:end_exclusive], so add 1 to the inclusive end index
    output_array[0, start_col : end_col_inclusive + 1] = primary_color

    # Convert the output numpy array back to a list of lists and return
    return output_array.tolist()