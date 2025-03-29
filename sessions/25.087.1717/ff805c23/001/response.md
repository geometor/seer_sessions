```python
import numpy as np

"""
The transformation rule is to extract a 5x5 subgrid from a fixed central location within the input grid.
Specifically, the subgrid corresponds to rows 11 through 15 and columns 10 through 14 (using 0-based indexing) of the input grid.
"""

def transform(input_grid):
    """
    Extracts a 5x5 subgrid from the center of the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 5x5 numpy array representing the extracted subgrid.
    """
    # Define the top-left corner row and column indices
    start_row = 11
    start_col = 10

    # Define the size of the subgrid
    size = 5

    # Calculate the end row and column indices (exclusive)
    end_row = start_row + size
    end_col = start_col + size

    # Extract the 5x5 subgrid using slicing
    # Slicing is [start_row:end_row, start_col:end_col]
    output_grid = input_grid[start_row:end_row, start_col:end_col]

    return output_grid

```