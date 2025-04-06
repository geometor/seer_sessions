"""
Transforms an input grid based on values in the first row.
Each non-zero value 'v' at column 'c' in the first row propagates downwards.
In odd-numbered rows (1, 3, 5,...), the value 'v' appears at columns c-1 and c+1 (if within bounds).
In even-numbered rows (2, 4, 6,...), the value 'v' appears at column c.
The original first row is preserved in the output.
Subsequent rows are initially filled with zeros and then populated by the propagation rule.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the propagation transformation to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Handle empty input grid case
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input_grid.
    # This preserves the first row and provides the base structure.
    # Although the description says subsequent rows are initially zero,
    # copying the input (which has zeros in those rows) achieves this.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell in the first row (row 0)
    for c in range(num_cols):
        # Get the value from the first row of the *original* input grid
        value_to_propagate = input_grid[0][c]

        # Only propagate non-zero values
        if value_to_propagate != 0:
            # Iterate through the subsequent rows (from row 1 downwards)
            for r in range(1, num_rows):
                # Check if the current row index 'r' is odd
                if r % 2 != 0:
                    # Odd row: place value at c-1 and c+1 (if within bounds)
                    # Check left neighbor column (c-1)
                    if c - 1 >= 0:
                        output_grid[r][c - 1] = value_to_propagate
                    # Check right neighbor column (c+1)
                    if c + 1 < num_cols:
                        output_grid[r][c + 1] = value_to_propagate
                # Else, the current row index 'r' is even
                else:
                    # Even row: place value directly below at column c
                    # Column 'c' is always within bounds here as it originated from row 0
                    output_grid[r][c] = value_to_propagate

    # Return the modified grid
    return output_grid