"""
Transforms a single-row grid by identifying a unique non-white color 'C' and filling 
the segments between consecutive occurrences of 'C' with that color.

Assumes the input grid contains exactly one row.
Assumes there is exactly one non-white color present in the input row.
Assumes there are at least two instances of the non-white color.
If these assumptions are not met, the original grid is returned.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_non_white_color_and_indices(row: np.ndarray) -> Tuple[Optional[int], Optional[np.ndarray]]:
    """
    Finds the unique non-white color and its indices in a row.

    Args:
        row: A numpy array representing the grid row.

    Returns:
        A tuple containing:
        - The non-white color value (int) or None if none or multiple are found.
        - A numpy array of indices where the color occurs, or None.
    """
    non_white_pixels = row[row != 0]
    unique_non_white = np.unique(non_white_pixels)

    if len(unique_non_white) != 1:
        # No non-white color or multiple different non-white colors found
        return None, None 
        
    color_c = unique_non_white[0]
    indices = np.where(row == color_c)[0]
    
    # Ensure indices are sorted (np.where usually returns them sorted, but being explicit)
    indices.sort() 
    
    return color_c, indices

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list containing a single list of integers representing the input row.

    Returns:
        A list containing a single list of integers representing the transformed row.
    """
    
    # --- Input Validation and Setup ---
    # Expecting a list containing exactly one list (the row)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        print("Warning: Input grid does not conform to expected single-row format. Returning original.")
        return input_grid

    # Extract the single row and convert to a numpy array
    row = np.array(input_grid[0], dtype=int)
    
    # Handle empty row case
    if row.size == 0:
        return input_grid 
        
    # --- Identify Color and Indices ---
    color_c, indices = find_non_white_color_and_indices(row)

    # If no single non-white color is found, or if indices are None, return original
    if color_c is None or indices is None:
        # This handles cases with only white pixels or multiple non-white colors
        return input_grid

    # If fewer than two anchor points exist, no segments can be filled
    if len(indices) < 2:
        return input_grid

    # --- Apply Transformation ---
    # Initialize the output row as a copy of the input row
    output_row = row.copy()

    # Iterate through consecutive pairs of indices
    # Example: if indices are [3, 11, 19], pairs are (3, 11) and (11, 19)
    for i in range(len(indices) - 1):
        start_index = indices[i]
        end_index = indices[i+1]
        
        # Fill the segment from start_index to end_index (inclusive) with color_c
        output_row[start_index : end_index + 1] = color_c

    # --- Format and Return Output ---
    # Convert the modified numpy row back into the List[List[int]] format
    output_grid = [output_row.tolist()]

    return output_grid