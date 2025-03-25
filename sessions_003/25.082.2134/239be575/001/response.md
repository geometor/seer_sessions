```python
"""
Selects a color from the input grid based on whether azure (8) or white (0) pixels form a straight, unbroken line across any row or column.
"""

import numpy as np

def check_straight_line(grid, color):
    """Checks if pixels of a given color form a straight line horizontally or vertically."""
    rows, cols = grid.shape

    # Check horizontal lines
    for row in range(rows):
        if all(grid[row, c] == color for c in range(cols)):
            return True

    # Check vertical lines
    for col in range(cols):
        if all(grid[r, col] == color for r in range(rows)):
            return True

    return False

def transform(input_grid):
    """
    Transforms the input grid according to the selection rule.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        int: The selected color (0 or 8).
    """
    grid = np.array(input_grid)

    # Check for straight line of azure (8)
    if check_straight_line(grid, 8):
        return 8

    # Check for straight line of white (0)
    if check_straight_line(grid, 0):
        return 0

    # Default return (shouldn't happen based on provided examples, but added for robustness)
    return -1 # Or raise an exception, depending on desired behavior
```