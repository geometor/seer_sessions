import numpy as np
from typing import List, Tuple

"""
Keep only the largest contiguous horizontal block of the non-white color found in the input row.
All other pixels, including isolated non-white pixels and smaller blocks, are set to white (0).
The background white pixels remain white.
This assumes the input is effectively a single row, as shown in the examples.
"""

def find_contiguous_blocks(row: np.ndarray, target_color: int) -> List[Tuple[int, int, int]]:
    """
    Finds all contiguous horizontal blocks of a target color in a 1D array (row).

    Args:
        row: The 1D numpy array representing the row.
        target_color: The integer color value to search for.

    Returns:
        A list of tuples, where each tuple represents a block:
        (start_index, end_index, length). Returns an empty list if no blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == target_color and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif pixel != target_color and in_block:
            # End of the current block
            in_block = False
            end_index = i # end_index is exclusive for slicing, but here inclusive for representation
            length = end_index - start_index
            blocks.append((start_index, end_index - 1, length)) # Store inclusive end index
            start_index = -1
        # Check if the last element is part of a block
        if i == len(row) - 1 and in_block:
            end_index = i + 1 # end_index is exclusive for slicing
            length = end_index - start_index
            blocks.append((start_index, end_index - 1, length)) # Store inclusive end index

    return blocks

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input grid (represented as a 1D list) by keeping only the 
    largest contiguous horizontal block of the non-white color.

    Args:
        input_grid: A list of integers representing the input row.

    Returns:
        A list of integers representing the transformed output row.
    """
    # Convert input list to numpy array for easier processing
    input_row = np.array(input_grid, dtype=int)
    
    # Initialize output grid with the same shape as input, filled with white (0)
    output_row = np.zeros_like(input_row)
    
    # Identify the primary non-white color
    # Assumes only one non-white color exists besides background (0)
    primary_color = 0
    unique_colors = np.unique(input_row)
    for color in unique_colors:
        if color != 0:
            primary_color = color
            break
            
    # If the input is all white, return the all-white output
    if primary_color == 0:
        return output_row.tolist()

    # Find all contiguous blocks of the primary color
    blocks = find_contiguous_blocks(input_row, primary_color)

    # If no blocks were found (shouldn't happen if primary_color > 0, but check anyway)
    if not blocks:
        return output_row.tolist()

    # Find the largest block (based on length)
    largest_block = max(blocks, key=lambda item: item[2]) # item[2] is the length

    # Transfer the largest block to the output grid
    start, end, _ = largest_block # Unpack the largest block's info
    # Note: 'end' from find_contiguous_blocks is inclusive
    output_row[start:end+1] = primary_color 

    # Convert the numpy array back to a list for the final output
    return output_row.tolist()
