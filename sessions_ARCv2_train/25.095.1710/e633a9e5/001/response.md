```python
"""
Expands a 3x3 grid of integers into a 5x5 grid.
The expansion follows specific factors for rows and columns.
The vertical expansion factors are [2, 1, 2], meaning the first input row maps to the first two output rows,
the second input row maps to the third output row, and the third input row maps to the last two output rows.
The horizontal expansion factors are [2, 1, 2], meaning the first input column maps to the first two output columns,
the second input column maps to the third output column, and the third input column maps to the last two output columns.
Each cell value from the input grid populates a rectangular block in the output grid determined by these expansion factors.
"""

import math
# No external libraries beyond standard Python are strictly necessary for this specific grid manipulation.

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 3x3 input grid into a 5x5 output grid based on specified
    row and column expansion factors.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 5x5 list of lists representing the expanded output grid.
    """

    # Define the expansion factors
    vertical_factors = [2, 1, 2]
    horizontal_factors = [2, 1, 2]

    # Calculate output dimensions
    output_rows = sum(vertical_factors)
    output_cols = sum(horizontal_factors)

    # Initialize the output grid with placeholders (e.g., 0 or None)
    # Using 0 as a placeholder, assuming input numbers are non-negative or distinction is clear.
    output_grid = [[0 for _ in range(output_cols)] for _ in range(output_rows)]

    # Track the starting row index for the current input row's block
    current_output_row = 0
    # Iterate through each row of the input grid
    for r in range(len(input_grid)):
        # Track the starting column index for the current input cell's block
        current_output_col = 0
        # Iterate through each column of the input grid for the current row
        for c in range(len(input_grid[r])):
            # Get the value from the input cell
            value_to_fill = input_grid[r][c]
            # Get the dimensions of the block to fill in the output grid
            block_height = vertical_factors[r]
            block_width = horizontal_factors[c]

            # Fill the corresponding block in the output grid
            for i in range(current_output_row, current_output_row + block_height):
                for j in range(current_output_col, current_output_col + block_width):
                    output_grid[i][j] = value_to_fill

            # Update the starting column index for the next block in this row
            current_output_col += block_width

        # Update the starting row index for the next row's blocks
        current_output_row += block_height

    return output_grid

```