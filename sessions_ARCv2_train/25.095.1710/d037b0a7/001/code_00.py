"""
Transforms a 2D grid by propagating non-zero values downwards within each column. 
For each column, non-zero values "fall" downwards, filling in any zero cells below them. 
The propagation continues iteratively until all zeros below a non-zero value in a column are filled by that value, or until the bottom of the grid is reached. If a cell is initially zero but gets filled by a value falling from above, that value continues to fall further down the column if there are more zeros below.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the downward propagation transformation to the input grid.

    Args:
        input_grid: A 2D list representing the input grid of integers.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Ensure input is not empty
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)

    # Perform transformations iteratively to ensure full propagation
    # The number of iterations needs to be at least height - 1 
    # to guarantee a value from the top row can reach the bottom row.
    # Iterating 'height' times is safe and covers all possibilities.
    for _ in range(height):  # Iterate enough times for values to fall to the bottom
        # Scan the grid row by row, starting from the second row (index 1)
        for r in range(1, height):
            # Iterate through each column
            for c in range(width):
                # Check if the current cell is zero
                is_current_zero = (output_grid[r][c] == 0)
                # Check if the cell directly above it is non-zero
                is_above_non_zero = (output_grid[r-1][c] != 0)

                # If the current cell is zero and the cell above is non-zero, propagate the value down
                if is_current_zero and is_above_non_zero:
                    output_grid[r][c] = output_grid[r-1][c]

    # Return the final transformed grid
    return output_grid