```python
import copy

"""
Transforms an input 3x3 grid by rotating its elements 180 degrees.
The element at position (r, c) in the input grid moves to position 
(2-r, 2-c) in the output grid (using 0-based indexing).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rotates a 3x3 grid 180 degrees.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A new 3x3 list of lists representing the rotated grid.
    """
    # Define the dimensions of the grid (assuming 3x3 based on examples)
    rows = len(input_grid)
    cols = len(input_grid[0]) # assumes rectangular grid

    # Initialize output_grid with the same dimensions, filled with a placeholder (e.g., 0)
    # Using deepcopy to ensure a separate structure if needed, though initializing with 0s is fine here.
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Perform transformations: Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the target position in the output grid for 180-degree rotation
            # For a grid of size rows x cols, the new row is (rows - 1 - r)
            # and the new column is (cols - 1 - c).
            # Since it's a 3x3 grid, rows=3 and cols=3.
            # So, new_r = 3 - 1 - r = 2 - r
            # And new_c = 3 - 1 - c = 2 - c
            new_r = (rows - 1) - r
            new_c = (cols - 1) - c

            # Place the element from the input grid into the calculated position in the output grid
            output_grid[new_r][new_c] = input_grid[r][c]

    # Return the newly created and populated output grid
    return output_grid
```