import numpy as np

"""
Extracts the 3x3 subgrid located in the top-right corner of the input grid.
The input grid is assumed to be 9x9. The extracted region corresponds to 
rows 0 through 2 and columns 6 through 8 (inclusive).
"""

def transform(input_grid):
    """
    Extracts the top-right 3x3 subgrid from the input grid.

    Args:
        input_grid (list of lists or numpy array): The input 9x9 grid.

    Returns:
        numpy array: The extracted 3x3 subgrid.
    """
    # Convert input to a numpy array for easier slicing
    grid = np.array(input_grid)

    # Define the coordinates for the top-right 3x3 subgrid
    start_row, end_row = 0, 3
    start_col, end_col = 6, 9

    # Extract the subgrid using numpy slicing
    # Select rows from start_row up to (but not including) end_row
    # Select columns from start_col up to (but not including) end_col
    output_grid = grid[start_row:end_row, start_col:end_col]

    # Return the extracted subgrid
    return output_grid
