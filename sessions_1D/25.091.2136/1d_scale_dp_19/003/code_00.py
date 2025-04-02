import numpy as np

"""
Fills the white (0) gap within a single-row grid between the rightmost pixel 
of a contiguous block of a non-white, non-maroon color and the first subsequent 
maroon (9) pixel with the color of that block. Assumes input is a 2D NumPy 
array with shape (1, N).
"""

def transform(input_grid):
    """
    Transforms the input grid based on the filling rule.

    Args:
        input_grid (np.ndarray): A 2D NumPy array, expected shape (1, N).

    Returns:
        np.ndarray: The transformed grid, same shape as input.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Check if the grid has at least one row
    if input_grid.shape[0] == 0 or input_grid.shape[1] == 0:
        return input_grid # Return empty or invalid grid as is

    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Work on the first row (index 0)
    row = output_grid[0]
    
    maroon_index = -1
    # 1. Find the index of the first maroon (9) pixel in the row.
    maroon_indices = np.where(row == 9)[0]
    if len(maroon_indices) > 0:
        maroon_index = maroon_indices[0]
    else:
        # If no maroon pixel is found, return the original grid unchanged.
        return input_grid 

    fill_color = -1
    block_end_index = -1
    # 2. Scan backwards from just before the maroon pixel to find the block end.
    for i in range(maroon_index - 1, -1, -1):
        pixel = row[i]
        # 3. Find the first pixel that is not white (0) and not maroon (9).
        if pixel != 0 and pixel != 9:
            fill_color = pixel
            block_end_index = i
            break # Found the block end pixel

    # 4. If no suitable block pixel is found before the maroon pixel, return the original grid.
    if block_end_index == -1:
        return input_grid

    # 5. Iterate from the pixel *after* the block ends up to *before* the maroon pixel.
    for i in range(block_end_index + 1, maroon_index):
        # 6. If a pixel in this range is white (0), change it to the fill_color in the output row.
        if row[i] == 0:
            row[i] = fill_color
            
    # The modifications were made directly on the row within output_grid
    return output_grid