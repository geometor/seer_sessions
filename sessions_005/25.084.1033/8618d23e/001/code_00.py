"""
Split the input grid horizontally in the middle (integer division), create an output grid one row taller and one column wider, initialized with maroon (9). Place the top half of the input grid in the top-left corner of the output grid. Place the bottom half of the input grid in the output grid, shifted down by one row and right by one column relative to its original position's corresponding split point. The remaining cells in the output grid, which form a cross/L-shape separating the two halves, remain maroon (9).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified split and shift rule.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed output grid as a list of lists.
    """
    # Convert input to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid.
    H, W = input_np.shape
    
    # Calculate the horizontal split index using integer division.
    split_row = H // 2
    
    # Determine the dimensions of the output grid.
    output_H = H + 1
    output_W = W + 1
    
    # Create a new output grid and initialize all cells with maroon (9).
    output_grid = np.full((output_H, output_W), 9, dtype=int)
    
    # Identify the top subgrid of the input.
    # Rows from 0 up to (but not including) split_row.
    # All columns (0 to W-1).
    top_half = input_np[0:split_row, :]
    
    # Copy this top subgrid to the output grid, placing its top-left corner at (0, 0).
    # Target region: rows 0 to split_row-1, columns 0 to W-1.
    if top_half.size > 0: # Ensure top_half is not empty
        output_grid[0:split_row, 0:W] = top_half
    
    # Identify the bottom subgrid of the input.
    # Rows from split_row up to (but not including) H.
    # All columns (0 to W-1).
    bottom_half = input_np[split_row:H, :]
    
    # Copy this bottom subgrid to the output grid, placing its top-left corner 
    # at position (split_row + 1, 1).
    # Target region: rows split_row + 1 to H, columns 1 to W.
    if bottom_half.size > 0: # Ensure bottom_half is not empty
        output_grid[split_row + 1 : H + 1, 1 : W + 1] = bottom_half
        
    # Convert the numpy array back to a list of lists for the expected output format.
    return output_grid.tolist()
