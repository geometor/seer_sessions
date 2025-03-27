"""
Transformation rule:
1. Initialize an output grid of the same dimensions as the input, filled with white (0).
2. Locate the coordinates (row, col) of the single azure (8) pixel and the single orange (7) pixel in the input grid.
3. Draw a horizontal line (fill the row) with azure (8) at the azure pixel's row index in the output grid.
4. Draw a vertical line (fill the column) with azure (8) at the azure pixel's column index in the output grid.
5. Draw a horizontal line (fill the row) with orange (7) at the orange pixel's row index in the output grid.
6. Draw a vertical line (fill the column) with orange (7) at the orange pixel's column index in the output grid.
7. Explicitly set the colors at the four intersection points:
    - (azure_row, azure_col) becomes azure (8).
    - (orange_row, orange_col) becomes orange (7).
    - (azure_row, orange_col) becomes orange (7).
    - (orange_row, azure_col) becomes red (2).
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the first occurrence of a pixel with the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return tuple(coords[0]) # return (row, col)
    return None

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input_grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # initialize output_grid with background color white (0)
    output_grid = np.zeros_like(input_np)

    # Find the coordinates of the azure (8) and orange (7) pixels
    azure_coords = find_pixel(input_np, 8)
    orange_coords = find_pixel(input_np, 7)

    if azure_coords is None or orange_coords is None:
        # Handle cases where one or both pixels are missing, though task description implies they exist
        # For now, return the empty grid if pixels aren't found
        return output_grid.tolist()

    row_azure, col_azure = azure_coords
    row_orange, col_orange = orange_coords

    # Draw the lines (step 3-6)
    # Fill the azure row and column
    output_grid[row_azure, :] = 8
    output_grid[:, col_azure] = 8
    # Fill the orange row and column
    output_grid[row_orange, :] = 7
    output_grid[:, col_orange] = 7

    # Set the specific intersection points (step 7)
    # This order ensures the correct colors override the initial line drawings
    output_grid[row_azure, col_azure] = 8  # Intersection of azure lines
    output_grid[row_orange, col_orange] = 7 # Intersection of orange lines
    output_grid[row_azure, col_orange] = 7 # Intersection of azure row and orange col
    output_grid[row_orange, col_azure] = 2  # Intersection of orange row and azure col

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
