import numpy as np

"""
The transformation rule is to extract a 5x5 subgrid from a fixed central location within the input grid.
Specifically, the subgrid corresponds to rows 11 through 15 and columns 10 through 14 (using 0-based indexing) of the input grid.

This hypothesis was tested and failed, indicating the transformation is more complex than simple fixed extraction. However, this code implements the stated hypothesis.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Extracts a 5x5 subgrid from a fixed location (rows 11-15, cols 10-14) in the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.
                                 Expected to be at least 16 rows and 15 columns.

    Returns:
        np.ndarray: A 5x5 numpy array representing the extracted subgrid.
    """
    # Define the top-left corner row and column indices (0-based)
    # These are based on the fixed location identified in the hypothesis.
    start_row = 11
    start_col = 10

    # Define the size of the subgrid to extract
    size = 5

    # Calculate the end row and column indices (exclusive) for slicing
    # end_row = start_row + size = 11 + 5 = 16
    # end_col = start_col + size = 10 + 5 = 15
    end_row = start_row + size
    end_col = start_col + size

    # Extract the 5x5 subgrid using numpy array slicing
    # The slice selects rows from start_row up to (but not including) end_row,
    # and columns from start_col up to (but not including) end_col.
    # Example: input_grid[11:16, 10:15]
    output_grid = input_grid[start_row:end_row, start_col:end_col]

    # Return the extracted subgrid
    return output_grid