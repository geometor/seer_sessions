```python
"""
Transforms an input grid by shifting all non-zero elements one position to the right.

The transformation rule involves:
1. Creating an output grid of the same dimensions as the input grid, initialized with zeros.
2. Iterating through each cell of the input grid.
3. If a cell contains a non-zero value, its value is copied to the cell one position to the right in the output grid, provided the new position is within the grid boundaries.
4. Cells originally occupied by shifted non-zero values, and cells not receiving a shifted value, remain zero in the output grid.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Shifts all non-zero elements in the input grid one column to the right.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Get grid dimensions
    if not input_grid or not input_grid[0]:
        return [] # Handle empty grid case
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid with the same dimensions as input_grid, filled with 0s
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Get the value from the input grid
            value = input_grid[r][c]

            # Check if the value is non-zero (representing a shape element)
            if value != 0:
                # Calculate the new column index (shift right by 1)
                new_c = c + 1

                # Check if the new column index is within the grid boundaries
                if new_c < num_cols:
                    # Place the non-zero value in the corresponding position in the output grid
                    output_grid[r][new_c] = value

    # Return the fully populated output grid
    return output_grid

```