"""
Identify a horizontal red segment and a vertical azure segment in the input grid. 
Modify the grid by extending the red segment across its entire row and filling the azure segment's entire column with azure. 
Mark the intersection of this new red row and azure column with yellow.
The order of operations is: fill column azure, fill row red, mark intersection yellow.
"""

import numpy as np

def find_pixel_coords(grid, color):
    """
    Finds the coordinates of the first pixel of a given color.
    Returns (row, col) or (None, None) if not found.
    Assumes the color exists uniquely enough to determine the required row/column.
    """
    rows, cols = np.where(grid == color)
    if len(rows) > 0:
        # Return the coordinates of the first found pixel
        # For this task, any pixel of the color is sufficient to find the row/col
        return rows[0], cols[0] 
    return None, None

def transform(input_grid):
    """
    Transforms the input grid based on the identified pattern:
    - Fills the column of the azure (8) segment with azure.
    - Fills the row of the red (2) segment with red.
    - Marks the intersection of the filled row and column with yellow (4).
    """
    # 1. Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 2. Identify the column index of the azure (8) vertical segment
    # We only need one coordinate to find the column
    _, azure_col = find_pixel_coords(input_grid, 8) 
    
    # 3. Identify the row index of the red (2) horizontal segment
    # We only need one coordinate to find the row
    red_row, _ = find_pixel_coords(input_grid, 2)

    # Check if both colors were found (essential elements for the transformation)
    if azure_col is None or red_row is None:
        # If essential elements are missing, return the original grid 
        # (though based on ARC task structure, we expect them to be present)
        print("Warning: Azure (8) or Red (2) color not found in input grid.")
        return output_grid 

    # 4. Modify the output grid: Fill the entire azure column with azure (8)
    output_grid[:, azure_col] = 8

    # 5. Modify the output grid: Fill the entire red row with red (2)
    # This overwrites the azure pixel at the intersection
    output_grid[red_row, :] = 2

    # 6. Modify the output grid: Mark the intersection pixel with yellow (4)
    # This overwrites the red pixel placed in the previous step at the intersection
    output_grid[red_row, azure_col] = 4

    # 7. Return the final modified grid
    return output_grid