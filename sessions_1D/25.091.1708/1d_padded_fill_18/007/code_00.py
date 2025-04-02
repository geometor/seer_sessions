"""
Identify the single non-white color (C) present in the input grid. Find the minimum (global_min_col) and maximum (global_max_col) column indices across all pixels of color C anywhere in the grid. Identify all rows (target_rows) that contain at least one pixel of color C. Initialize the output grid as a copy of the input. For each row index r, if r is in target_rows, fill the horizontal segment in the output grid's row r from global_min_col to global_max_col (inclusive) with color C. Rows not in target_rows remain unchanged.
"""

import numpy as np

def find_non_white_pixels(grid):
    """
    Finds the coordinates and color of all non-white (value != 0) pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (color, row_indices, col_indices)
               - color (int): The non-white color found (assumes only one). None if none found.
               - row_indices (np.ndarray): Array of row indices of non-white pixels.
               - col_indices (np.ndarray): Array of column indices of non-white pixels.
               Returns (None, None, None) if no non-white pixels are found.
    """
    row_indices, col_indices = np.where(grid != 0)
    if len(row_indices) == 0:
        return None, None, None  # No non-white pixels found

    # Assume only one non-white color exists and get it from the first found pixel
    color = grid[row_indices[0], col_indices[0]]
    
    return color, row_indices, col_indices

def get_global_bounds(col_indices):
    """
    Calculates the minimum and maximum column indices from an array of indices.

    Args:
        col_indices (np.ndarray): Array of column indices.

    Returns:
        tuple: (min_col, max_col). Returns (None, None) if input is empty.
    """
    if col_indices is None or not col_indices.size: # Check if the array is None or empty
         return None, None
    min_col = np.min(col_indices)
    max_col = np.max(col_indices)
    return min_col, max_col

def get_target_rows(row_indices):
    """
    Finds the unique row indices from an array of indices.

    Args:
        row_indices (np.ndarray): Array of row indices.

    Returns:
        np.ndarray: Sorted array of unique row indices. Returns empty array if input is None.
    """
    if row_indices is None:
        return np.array([], dtype=int)
    return np.unique(row_indices)


def transform(input_grid):
    """
    Fills horizontal segments in specific rows based on the global horizontal
    extent of a single non-white color.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the non-white pixels, their color, and their row/column indices
    primary_color, row_indices, col_indices = find_non_white_pixels(input_grid)
    
    # If no non-white pixels are found, return the original grid copy
    if primary_color is None:
        return output_grid
        
    # Calculate the global minimum and maximum column indices for the primary color
    global_min_col, global_max_col = get_global_bounds(col_indices)
    
    # Check if bounds calculation was successful (handles case of no non-white pixels found, though already checked)
    if global_min_col is None:
         return output_grid # Should not happen if primary_color is not None, but safe check

    # Identify the unique rows containing the primary color
    target_rows = get_target_rows(row_indices)

    # Iterate through the identified target rows
    for r in target_rows:
        # Fill the horizontal segment in the output grid for the current target row
        # using the global column bounds and the primary color.
        # The slice includes global_min_col and global_max_col.
        output_grid[r, global_min_col : global_max_col + 1] = primary_color

    return output_grid