"""
Translate a single non-white object horizontally based on its position relative 
to the side edges, keeping its vertical position unchanged.

The transformation identifies the single contiguous non-white object in the input grid. 
It calculates the empty horizontal space (gap) before and after the object's 
bounding box. If the gap before is less than or equal to the gap after, 
the object is shifted left to align its left edge with the grid's left edge. 
If the gap before is greater than the gap after, the object is shifted left 
by half the size of the gap before (rounded down for the gap before + 1). 
The object's vertical position remains the same. The output grid has the same 
dimensions as the input grid and is initially filled with the background color (white, 0).
"""

import numpy as np
import math

def find_object_pixels(grid):
    """
    Identifies all non-background (non-zero) pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (row, column, color) 
              for a non-background pixel. Returns an empty list if no object is found.
    """
    object_pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0: # Assuming 0 is the background color
                object_pixels.append((r, c, color))
    return object_pixels

def calculate_bounding_box(object_pixels):
    """
    Calculates the minimum and maximum row and column indices 
    of the bounding box containing the object pixels.

    Args:
        object_pixels (list): A list of (row, column, color) tuples.

    Returns:
        dict: A dictionary containing 'min_row', 'min_col', 'max_row', 'max_col', 
              or None if object_pixels is empty.
    """
    if not object_pixels:
        return None
    
    rows = [r for r, c, color in object_pixels]
    cols = [c for r, c, color in object_pixels]
    
    return {
        'min_row': min(rows),
        'min_col': min(cols),
        'max_row': max(rows),
        'max_col': max(cols)
    }

def transform(input_grid):
    """
    Transforms the input grid by translating the single non-white object 
    horizontally based on its position relative to the side edges, 
    keeping its vertical position unchanged.

    Args:
        input_grid (list or np.array): The input grid represented as a list of lists or numpy array.

    Returns:
        np.array: The transformed output grid as a numpy array.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # 1. Initialize the output grid with the background color (white, 0).
    output_grid = np.zeros_like(input_grid_np)

    # 2. Identify all non-white pixels forming the object.
    object_pixels = find_object_pixels(input_grid_np)

    # If no object is found, return the empty grid
    if not object_pixels:
        return output_grid

    # 3. Determine the bounding box of the object.
    bbox = calculate_bounding_box(object_pixels)
    min_col = bbox['min_col']
    max_col = bbox['max_col']
    
    # 4. Calculate the horizontal gap before the object.
    gap_before = min_col

    # 5. Calculate the horizontal gap after the object.
    gap_after = width - 1 - max_col

    # 6. Determine the horizontal shift amount (shift_left_amount).
    shift_left_amount = 0
    if gap_before <= gap_after:
        # a. If gap before is less than or equal to gap after, shift to left edge.
        shift_left_amount = min_col 
    else:
        # b. If gap before is greater than gap after, shift left by floor((gap_before + 1) / 2).
        shift_left_amount = (gap_before + 1) // 2 # Integer division provides floor

    # 7. For each non-background pixel in the input:
    for r, c, color in object_pixels:
        # a. Calculate its new column index.
        new_c = c - shift_left_amount
        # b. The row index remains unchanged.
        new_r = r
        
        # c. Ensure the new coordinates are within the grid bounds
        #    (This check is technically redundant if logic is perfect but safe)
        if 0 <= new_r < height and 0 <= new_c < width:
             # d. Set the pixel at the new coordinates in the output grid.
            output_grid[new_r, new_c] = color

    # 8. Return the completed output grid.
    return output_grid