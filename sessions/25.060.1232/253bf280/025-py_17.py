"""
1.  **Identify Columns with Azure Markers:** Find all columns in the input grid that contain one or more azure (color code 8) pixels.
2.  **Find Topmost and Bottommost Azure Pixels:** For each column identified in step 1, determine the row index of the topmost azure pixel and the row index of the bottommost azure pixel.
3.  **Draw Green Vertical Lines:** For each column, if there are at least two azure pixels, draw a vertical line of green (color code 3) pixels between the topmost and bottommost azure pixels (exclusive of the azure pixels' rows). Specifically, start the green line one row below the topmost azure pixel and end it one row above the bottommost azure pixel.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds coordinates of all pixels of a specified color."""
    return np.array(np.where(grid == color)).T.tolist()

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find all azure pixels
    azure_pixels = find_pixels_by_color(input_grid, 8)

    # Group azure pixels by column
    columns_with_azure = {}
    for row, col in azure_pixels:
        if col not in columns_with_azure:
            columns_with_azure[col] = []
        columns_with_azure[col].append(row)

    # Draw green lines in each column with at least two azure pixels
    for col, row_indices in columns_with_azure.items():
        if len(row_indices) >= 2:
            # Find topmost and bottommost row indices
            topmost_row = min(row_indices)
            bottommost_row = max(row_indices)

            # Draw the green line (exclusive of the azure pixels)
            for row in range(topmost_row + 1, bottommost_row):
                output_grid[row, col] = 3

    return output_grid