```python
"""
Crop the input grid to the minimal bounding box containing the non-white object.

1. Scan the input grid to locate all pixels that have a color other than white (0).
2. Find the coordinates (row and column indices) of the top-most, bottom-most,
   left-most, and right-most non-white pixels.
3. Define a rectangular region (bounding box) using these minimum and maximum row
   and column indices.
4. Create the output grid by extracting the pixels from the input grid that fall
   within this defined bounding box.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the minimal bounding box containing non-white pixels from the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the cropped output grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)

    # Find the coordinates (rows, cols) of all non-white pixels (value != 0)
    non_white_coords = np.argwhere(grid_np != 0)

    # If there are no non-white pixels, return an empty grid or handle as appropriate
    # Based on examples, we expect at least one non-white pixel.
    if non_white_coords.size == 0:
        return [] # Or potentially return the original grid, depends on spec if this happens

    # Determine the minimum and maximum row and column indices
    min_row = non_white_coords[:, 0].min()
    max_row = non_white_coords[:, 0].max()
    min_col = non_white_coords[:, 1].min()
    max_col = non_white_coords[:, 1].max()

    # Extract the subgrid defined by the bounding box
    # Slicing includes the start index but excludes the end index, so add 1 to max indices
    output_grid_np = grid_np[min_row : max_row + 1, min_col : max_col + 1]

    # Convert the NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid

```