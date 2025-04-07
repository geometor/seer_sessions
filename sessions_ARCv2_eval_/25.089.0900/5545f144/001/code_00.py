"""
1. Determine the most frequent color in the input grid; this is the background color.
2. Iterate through the columns of the input grid, starting from the leftmost column (index 0).
3. For each column, check if all pixels in that column have the same color and if that color is different from the background color.
4. Identify the index of the *first* column that satisfies these conditions (the delimiter column).
5. Create the output grid by taking a slice of the input grid that includes all rows and all columns from index 0 up to, but not including, the index of the identified delimiter column.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    flat_grid = grid.flatten()
    counts = Counter(flat_grid)
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_delimiter_column(grid, background_color):
    """Finds the index of the first vertical delimiter column."""
    num_rows, num_cols = grid.shape
    for col_idx in range(num_cols):
        column = grid[:, col_idx]
        # Check if all elements in the column are the same
        if np.all(column == column[0]):
            # Check if the column color is different from the background
            if column[0] != background_color:
                return col_idx  # Found the first delimiter column
    return -1 # Should not happen based on examples, but good practice

def transform(input_grid):
    """
    Extracts the portion of the input grid to the left of the first 
    vertical delimiter line of a non-background color.
    """
    # Convert input list of lists to numpy array for easier slicing
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Determine the background color
    background_color = find_background_color(grid_np)
    
    # 2. & 3. & 4. Find the first delimiter column index
    delimiter_col_idx = find_delimiter_column(grid_np, background_color)
    
    # 5. Create the output grid by slicing
    # Check if a delimiter was found (it should be based on task description)
    if delimiter_col_idx != -1:
        # Slice the grid: take all rows, and columns from 0 up to delimiter_col_idx
        output_grid_np = grid_np[:, :delimiter_col_idx]
    else:
        # If no delimiter found (unexpected), return the original grid or handle error
        # Based on the examples, a delimiter always seems to exist.
        # Returning the original might be a safe default if the pattern breaks.
        output_grid_np = grid_np 

    # Convert back to list of lists if necessary for the environment
    output_grid = output_grid_np.tolist()

    return output_grid