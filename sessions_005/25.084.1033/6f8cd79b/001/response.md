```python
"""
Creates a one-pixel thick border of azure (8) around the perimeter of the input grid, leaving the interior pixels unchanged (typically white, 0).
"""

import numpy as np

def transform(input_grid):
    """
    Applies a border transformation to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the output grid with an azure border.
    """
    # Convert the input list of lists to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)

    # Get the dimensions (height, width) of the grid
    height, width = grid.shape

    # Create a copy of the input grid to modify, ensuring the original is unchanged
    output_grid = np.copy(grid)

    # Define the border color
    border_color = 8  # azure

    # Set the top row to the border color
    if height > 0:
        output_grid[0, :] = border_color

    # Set the bottom row to the border color
    if height > 1:
        output_grid[height - 1, :] = border_color

    # Set the first column to the border color
    if width > 0:
        output_grid[:, 0] = border_color

    # Set the last column to the border color
    if width > 1:
        output_grid[:, width - 1] = border_color

    # Convert the resulting numpy array back to a list of lists for the standard output format
    return output_grid.tolist()

```