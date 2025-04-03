import numpy as np

"""
Transforms an input grid by identifying a single contiguous horizontal segment of 
a non-white color in the first row and shifting this segment exactly two 
columns to the right. The output grid has the same dimensions as the input, 
initially filled with the background color (white, 0). The space vacated by 
the segment becomes white, and the space occupied by the shifted segment takes 
the segment's original color. It assumes the input grid has at least one row 
and the colored segment, if present, is in the first row where a non-white 
pixel appears.
"""

def find_colored_segment(grid):
    """
    Finds the row index, start column index (inclusive), end column index 
    (exclusive), and color of the first contiguous horizontal non-white segment.

    Args:
        grid (np.array): The input 2D grid.

    Returns:
        tuple: (row_index, start_col, end_col, color) or (-1, -1, -1, 0) if no 
               segment is found.
    """
    if grid.shape[0] == 0: 
        return -1, -1, -1, 0 # Empty grid

    target_row_idx = -1
    # Iterate through rows to find the first one containing any non-white pixel
    for r_idx, row in enumerate(grid):
        if np.any(row != 0):
            target_row_idx = r_idx
            break
            
    # If no non-white pixel was found in any row, return not found
    if target_row_idx == -1: 
        return -1, -1, -1, 0 

    # Analyze the target row to find the segment
    arr = grid[target_row_idx]
    start_col = -1
    color = 0
    for c_idx, pixel in enumerate(arr):
        # Found the start of a potential segment
        if pixel != 0 and start_col == -1:
            start_col = c_idx
            color = pixel
        
        # If we are inside a segment, check for its end
        if start_col != -1:
            is_last_pixel = (c_idx == len(arr) - 1)
            # Segment ends if next pixel is different color or we are at the end
            is_different_next = (not is_last_pixel and arr[c_idx+1] != color)
            if pixel == color and (is_last_pixel or is_different_next):
                end_col = c_idx + 1 # End index is exclusive
                return target_row_idx, start_col, end_col, color

    # If loop finishes without returning, it means either the row was all white 
    # (handled earlier) or something unexpected happened.
    return -1, -1, -1, 0

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid with the same shape as input, filled with background color (0)
    output_grid = np.zeros_like(input_np)
    
    # 1. Identify the single contiguous horizontal segment of non-white pixels
    row_idx, start_col, end_col, segment_color = find_colored_segment(input_np)
    
    # Proceed only if a segment was found
    if row_idx != -1:
        # 2. Calculate the new column positions by shifting right by 2
        new_start_col = start_col + 2
        new_end_col = end_col + 2
        
        # 3. Place the segment into the output grid at the new positions
        # Ensure indices stay within the grid bounds during assignment.
        # Numpy slicing handles cases where the new segment might partially 
        # or fully go off the right edge. We only need to make sure the row index
        # and the start/end indices are non-negative for slicing.
        
        # Determine the actual columns to fill in the output grid, considering boundaries
        actual_start = max(0, new_start_col)
        actual_end = min(output_grid.shape[1], new_end_col) # shape[1] is width
        
        # Only attempt assignment if there's a valid range within bounds
        if actual_start < actual_end:
             output_grid[row_idx, actual_start:actual_end] = segment_color
             
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
