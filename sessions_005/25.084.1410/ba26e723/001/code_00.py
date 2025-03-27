import numpy as np

"""
Transforms the input grid by changing specific yellow (4) pixels to magenta (6)
based on patterns related to the column index and the starting color of the top row.

The transformation rules depend on whether the top-left pixel (0, 0) is yellow (4) or white (0).

1. If the pixel at (0, 0) is yellow (4):
   - Row 0: Change yellow (4) to magenta (6) if the column index `col` is divisible by 6.
   - Row 1: Change yellow (4) to magenta (6) if the column index `col` is divisible by 3.
   - Row 2: Change yellow (4) to magenta (6) if `col >= 3` and `(col - 3)` is divisible by 6.

2. If the pixel at (0, 0) is white (0):
   - Row 0: Change yellow (4) to magenta (6) if `col >= 3` and `(col - 3)` is divisible by 6.
   - Row 1: Change yellow (4) to magenta (6) if the column index `col` is divisible by 3.
   - Row 2: Change yellow (4) to magenta (6) if the column index `col` is divisible by 6.

White (0) pixels remain unchanged in all cases.
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation and indexing
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()
    # Get the dimensions of the grid (height is always 3, width varies)
    height, width = grid.shape

    # Check the pattern based on the color of the pixel at (0, 0)
    # Pattern A: Row 0 starts yellow (4), Row 2 starts white (0)
    # Pattern B: Row 0 starts white (0), Row 2 starts yellow (4)
    is_pattern_a = grid[0, 0] == 4

    # Iterate through each column of the grid
    for col in range(width):
        # Apply rule for Row 1 (Middle Row) - This rule is independent of the pattern
        # If the pixel is yellow (4) and the column index is divisible by 3, change it to magenta (6)
        if grid[1, col] == 4 and col % 3 == 0:
            output_grid[1, col] = 6

        # Apply rules for Row 0 (Top Row) and Row 2 (Bottom Row) based on the detected pattern
        if is_pattern_a:
            # Apply rules for Pattern A
            # Row 0: If pixel is yellow (4) and column index is divisible by 6, change to magenta (6)
            if grid[0, col] == 4 and col % 6 == 0:
                output_grid[0, col] = 6
            # Row 2: If pixel is yellow (4), column index >= 3, and (column index - 3) is divisible by 6, change to magenta (6)
            if grid[2, col] == 4 and col >= 3 and (col - 3) % 6 == 0:
                output_grid[2, col] = 6
        else:
            # Apply rules for Pattern B
            # Row 0: If pixel is yellow (4), column index >= 3, and (column index - 3) is divisible by 6, change to magenta (6)
            if grid[0, col] == 4 and col >= 3 and (col - 3) % 6 == 0:
                output_grid[0, col] = 6
            # Row 2: If pixel is yellow (4) and column index is divisible by 6, change to magenta (6)
            if grid[2, col] == 4 and col % 6 == 0:
                output_grid[2, col] = 6

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()