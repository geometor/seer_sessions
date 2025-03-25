"""
The input grid is transformed into the output grid by reversing the order of the rows.
In other words perform a vertical flip of the grid.
The first row of the input will become the last row of the output.
The second row of the input will become the second to last row of the output and so on.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing the order of its rows.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Convert the input grid to a NumPy array if it isn't already.
    input_grid = np.array(input_grid)

    # Reverse the order of rows using NumPy's flip function along the vertical axis (axis=0).
    output_grid = np.flip(input_grid, axis=0)

    return output_grid