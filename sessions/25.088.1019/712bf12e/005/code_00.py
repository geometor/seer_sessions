"""
Paint upwards from red pixels in the input grid.
Initialize the output grid as a copy of the input grid.
Identify all red (2) pixels in the input grid. These are 'source' pixels.
For each source pixel at (r_source, c):
Iterate upwards from the row directly above the source (r = r_source - 1) towards row 0.
At each step (row, c), check the color of the pixel in the *input* grid.
If the input pixel at (row, c) is white (0), change the corresponding pixel in the *output* grid to red (2).
If the input pixel at (row, c) is not white (any non-zero color), stop the upward painting process for this specific source pixel and column.
Continue this process for all identified source pixels.
Pixels not painted retain their original color from the input grid. Obstacle pixels (non-white) block painting but remain unchanged.
"""

import numpy as np

def find_pixels_by_color(grid, color_value):
    """
    Finds the coordinates of all pixels with a specific color value.

    Args:
        grid (np.array): The input grid.
        color_value (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple is (row, column) coordinate.
    """
    rows, cols = np.where(grid == color_value)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Applies the upward painting transformation based on red pixels in the input grid.

    Args:
        input_grid (np.array): A 2D NumPy array representing the input grid.

    Returns:
        np.array: A 2D NumPy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape

    # Find all red (2) pixels (source pixels) in the input grid
    source_pixel_coords = find_pixels_by_color(input_grid, 2)

    # Iterate through each found source pixel
    for r_source, c in source_pixel_coords:
        # Start checking from the row directly above the source pixel
        current_row = r_source - 1

        # Paint upwards as long as we are within the grid bounds (row >= 0)
        while current_row >= 0:
            # Check the color of the cell in the *input* grid at the current position
            if input_grid[current_row, c] == 0:
                # If it's white (0) in the input, paint it red (2) in the output grid
                output_grid[current_row, c] = 2
                # Move to the next row above
                current_row -= 1
            else:
                # If it's not white (it's an obstacle in the input grid), stop painting upwards for this column/source
                break
        # Loop terminates if current_row becomes < 0 (top edge reached) or if an obstacle was hit (break called)

    # Return the modified grid
    return output_grid