```python
import numpy as np

"""
Transforms the input grid based on the following rule:
For each column, find the topmost non-white pixel. If found, fill all pixels
in that column from that row downwards with the color of that topmost pixel.
If a column contains only white pixels, it remains unchanged.
"""

# Imports
import numpy as np

# Helper function to find the topmost non-white pixel in a column
def _find_topmost_non_white(grid, col_index):
    """
    Finds the topmost non-white pixel in a specific column of the grid.

    Args:
        grid (np.array): The input grid.
        col_index (int): The index of the column to search.

    Returns:
        tuple: A tuple containing (row_index, color) of the topmost non-white pixel.
               Returns (-1, None) if no non-white pixel is found in the column.
    """
    height = grid.shape[0]
    # Iterate through rows from top to bottom
    for r in range(height):
        color = grid[r, col_index]
        # Check if the pixel color is not white (0)
        if color != 0:
            return r, color  # Return the row index and color
    # Return default values if no non-white pixel is found
    return -1, None

def transform(input_grid):
    """
    Applies a column-wise downward fill transformation to the input grid.

    For each column:
    1. Finds the first non-white pixel from the top.
    2. If found, it fills all cells in that column from that pixel's row down
       to the bottom with the color of that first non-white pixel.
    3. If a column contains only white pixels, it remains unchanged.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Initialize the output grid as a copy of the input grid.
    # Modifications will be made directly to this copy.
    output_grid = grid.copy()

    # Iterate through each column index 'c' from 0 to width - 1
    for c in range(width):
        # Use the helper function to find the topmost non-white pixel and its row
        found_row, found_color = _find_topmost_non_white(grid, c)

        # Check if a non-white pixel was actually found in the column
        if found_row != -1:
            # If found, iterate through the rows starting from the 'found_row'
            # down to the last row ('height' - 1)
            for r_fill in range(found_row, height):
                # Set the color of the pixel at (r_fill, c) in the output grid
                # to the 'found_color'
                output_grid[r_fill, c] = found_color
        # If found_row is -1 (column is all white), no action is needed
        # because output_grid started as a copy of the input grid.

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()
```