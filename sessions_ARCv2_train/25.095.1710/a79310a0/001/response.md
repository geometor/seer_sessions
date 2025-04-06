```python
"""
Transforms an input grid by shifting all cells containing the value 8 down by one row, changing their value to 2. Cells containing 0 remain unchanged. Cells shifted beyond the bottom boundary are discarded.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    # Get the dimensions of the input grid
    num_rows = len(input_grid)
    if num_rows == 0:
        return []
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return [[] for _ in range(num_rows)] # Return grid of empty rows if cols is 0

    # Initialize the output grid with the same dimensions as the input, filled with 0s
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Check if the current input cell contains the value 8
            if input_grid[r][c] == 8:
                # Calculate the target row index for the output grid (one row down)
                target_r = r + 1

                # Check if the target row index is within the grid's vertical bounds
                if target_r < num_rows:
                    # Set the corresponding cell in the output grid to 2
                    output_grid[target_r][c] = 2
            # Note: Cells with 0 in the input implicitly remain 0 in the output
            # because the output grid was initialized with 0s.

    # Return the completed output grid
    return output_grid
```