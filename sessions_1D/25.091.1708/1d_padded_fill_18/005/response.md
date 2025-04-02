```python
"""
Identify the single non-white color (C) present in the input grid. Find the minimum (global_min_col) and maximum (global_max_col) column indices across all pixels of color C. Identify all rows (target_rows) that contain at least one pixel of color C. Initialize the output grid as a copy of the input. For each row index r, if r is in target_rows, fill the segment in the output grid's row r from global_min_col to global_max_col (inclusive) with color C. Rows not in target_rows remain unchanged.
"""

import numpy as np

def find_non_white_pixels(grid):
    """Finds the coordinates and color of non-white pixels."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None, None, None  # No non-white pixels found
    
    # Assuming only one non-white color exists
    color = grid[rows[0], cols[0]]
    coordinates = list(zip(rows, cols))
    return color, coordinates, (rows, cols) # Return color, list of (r,c) tuples, and separate row/col arrays

def get_global_bounds(col_indices):
    """Calculates the minimum and maximum column indices."""
    if not col_indices.size: # Check if the array is empty
         return None, None
    min_col = np.min(col_indices)
    max_col = np.max(col_indices)
    return min_col, max_col

def get_target_rows(row_indices):
    """Finds the unique row indices containing non-white pixels."""
    return np.unique(row_indices)


def transform(input_grid):
    """
    Fills horizontal segments in specific rows based on the global horizontal
    extent of a single non-white color.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the non-white pixels, their color, and their coordinates
    primary_color, _, indices = find_non_white_pixels(input_grid)
    
    # If no non-white pixels are found, return the original grid copy
    if primary_color is None:
        return output_grid
        
    row_indices, col_indices = indices

    # Calculate the global minimum and maximum column indices for the primary color
    global_min_col, global_max_col = get_global_bounds(col_indices)

    # Identify the unique rows containing the primary color
    target_rows = get_target_rows(row_indices)

    # Iterate through the identified target rows
    for r in target_rows:
        # Fill the horizontal segment in the output grid for the current target row
        # using the global column bounds and the primary color
        # Ensure slicing includes the max_col index
        output_grid[r, global_min_col : global_max_col + 1] = primary_color

    return output_grid
```