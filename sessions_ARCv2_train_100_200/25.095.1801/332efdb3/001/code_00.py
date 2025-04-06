"""
Transforms an input grid (assumed to be all zeros) into an output grid of the same dimensions.
The output grid follows a specific pattern:
- Rows with even indices are filled entirely with 1s.
- Rows with odd indices have an alternating pattern of 1s and 0s, starting with 1 in the first column (index 0), 0 in the second (index 1), 1 in the third (index 2), and so on.
"""

import math  # Although not strictly needed for this logic, included as per template suggestion
import copy # To create a deep copy if needed, though direct creation is better here

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the pattern transformation to the input grid dimensions.

    Args:
        input_grid: A list of lists of integers (representing the input grid).

    Returns:
        A list of lists of integers representing the transformed output grid.
    """
    # Determine the dimensions of the grid
    if not input_grid:
        return []
    num_rows = len(input_grid)
    if num_rows == 0 or not input_grid[0]:
         return [[] for _ in range(num_rows)] # Handle empty rows or empty grid
    num_cols = len(input_grid[0])

    # Initialize the output grid with the correct dimensions
    # We can initialize it with zeros and then fill it, or create it row by row.
    # Let's create it row by row based on the logic.
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the output grid using its row index i and column index j
    for i in range(num_rows):
        # Check if the row index i is even
        if i % 2 == 0:
            # If i is even, set all cells in this row to 1
            for j in range(num_cols):
                output_grid[i][j] = 1
        else:
            # If i is odd, apply the alternating pattern based on column index j
            for j in range(num_cols):
                # Check if the column index j is even
                if j % 2 == 0:
                    # If j is even, set the cell value to 1
                    output_grid[i][j] = 1
                else:
                    # If j is odd, set the cell value to 0
                    output_grid[i][j] = 0

    # Return the completed output grid
    return output_grid
