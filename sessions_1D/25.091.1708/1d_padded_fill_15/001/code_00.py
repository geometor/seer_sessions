import numpy as np

"""
Transformation Rule:
1. Identify the single non-white color (C) present in the input row (1D grid).
2. Find all column indices where color C appears.
3. Determine the minimum (min_col) and maximum (max_col) index among these positions.
4. Create an output row of the same length, initially filled with the background color (white, 0).
5. Fill the segment of the output row from min_col to max_col (inclusive) with color C.
"""

def find_non_background_color(grid, background_color=0):
    """Finds the single color in the grid that is not the background color."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != background_color:
            return color
    return None # Return None if only background color is present

def transform(input_grid):
    """
    Fills the segment between the first and last occurrence of the non-background color.

    Args:
        input_grid (np.ndarray): A 1D numpy array representing the input row.

    Returns:
        np.ndarray: A 1D numpy array representing the transformed output row.
    """
    # Ensure input is treated as a 1D array for processing
    input_row = input_grid.flatten()
    
    # Identify the non-white (non-zero) color
    fill_color = find_non_background_color(input_row, background_color=0)

    # If no non-background color is found, return the grid as is
    if fill_color is None:
        return input_grid # Or np.copy(input_grid) if modification is a concern

    # Find all indices where the fill_color appears
    indices = np.where(input_row == fill_color)[0]

    # If the color doesn't actually appear (shouldn't happen if fill_color is not None, but safe check)
    if len(indices) == 0:
        return input_grid

    # Determine the minimum and maximum index
    min_col = np.min(indices)
    max_col = np.max(indices)

    # Create the output grid, initialized with the background color (0)
    output_grid = np.zeros_like(input_grid) # Maintain original shape (e.g., 1xN)
    output_row = output_grid.flatten() # Work with the flattened version

    # Fill the segment between min_col and max_col (inclusive) with the fill_color
    output_row[min_col : max_col + 1] = fill_color

    return output_grid