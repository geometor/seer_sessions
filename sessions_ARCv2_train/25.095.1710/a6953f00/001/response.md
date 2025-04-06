```python
import math
# Potential standard library imports if needed later, e.g., re, collections

"""
Transforms an input grid of integers by extracting a specific 2x2 subgrid.
If the number of rows in the input grid is even, the top-right 2x2 subgrid is extracted.
If the number of rows is odd, the top-left 2x2 subgrid is extracted.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts a 2x2 subgrid from the input grid based on the parity of the number of rows.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A 2x2 list of lists representing the extracted subgrid.
    """

    # Determine the dimensions of the input grid
    num_rows = len(input_grid)
    # Assuming a non-empty grid, get the number of columns from the first row
    num_cols = len(input_grid[0]) if num_rows > 0 else 0

    # Initialize the output grid (always 2x2)
    output_grid = [[0, 0], [0, 0]]

    # Check if the number of rows is even or odd
    if num_rows % 2 == 0:
        # Even number of rows: Extract top-right 2x2 subgrid
        # Ensure grid is large enough for extraction
        if num_rows >= 2 and num_cols >= 2:
            output_grid[0][0] = input_grid[0][num_cols - 2]
            output_grid[0][1] = input_grid[0][num_cols - 1]
            output_grid[1][0] = input_grid[1][num_cols - 2]
            output_grid[1][1] = input_grid[1][num_cols - 1]
        else:
            # Handle cases where the grid is too small for the required extraction
            # Based on examples, this shouldn't happen, but defensive coding is good.
            # Returning an empty or partially filled grid might be options,
            # but let's stick to the observed pattern for now.
             pass # Or raise an error, or return default empty grid

    else:
        # Odd number of rows: Extract top-left 2x2 subgrid
        # Ensure grid is large enough for extraction
        if num_rows >= 2 and num_cols >= 2:
            output_grid[0][0] = input_grid[0][0]
            output_grid[0][1] = input_grid[0][1]
            output_grid[1][0] = input_grid[1][0]
            output_grid[1][1] = input_grid[1][1]
        else:
            # Handle cases where the grid is too small
            pass # Or raise an error, or return default empty grid


    # Return the extracted 2x2 subgrid
    return output_grid

```