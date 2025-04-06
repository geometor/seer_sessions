"""
Transforms a 2D grid of integers by replacing each occurrence of the number 6 
with the number 2, while keeping the number 7 unchanged. The dimensions of the 
output grid are identical to the input grid.
"""

import copy # Used only if initializing the output grid by deep copying the input initially

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a cell-wise transformation to the input grid.
    Replaces 6 with 2, leaves 7 as 7.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Get the dimensions of the input grid
    if not input_grid:
        return []
    num_rows = len(input_grid)
    if not input_grid[0]:
         # Handle case of empty rows if necessary, although examples don't show this
         return [[] for _ in range(num_rows)]
    num_cols = len(input_grid[0])

    # Initialize an output grid with the same dimensions, filled with a placeholder (e.g., 0)
    # Alternatively, could deep copy input_grid and modify in place, but creating a new
    # grid is often clearer for transformations.
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Read the value from the input grid cell
            cell_value = input_grid[r][c]

            # Apply the transformation rule
            if cell_value == 6:
                # If the value is 6, place 2 in the output grid
                output_grid[r][c] = 2
            elif cell_value == 7:
                 # If the value is 7, place 7 in the output grid
                output_grid[r][c] = 7
            # else:
                # Optional: Handle unexpected values if necessary
                # For this specific problem based on examples, only 6 and 7 appear.
                # If other numbers could appear, define their behavior here.
                # e.g., output_grid[r][c] = cell_value # Keep other values unchanged
                # or raise ValueError(f"Unexpected value {cell_value} at ({r},{c})")

    # Return the completed output grid
    return output_grid
