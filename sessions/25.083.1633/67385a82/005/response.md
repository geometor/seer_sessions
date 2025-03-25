```python
"""
1.  **Scan the Input Grid:** Examine the entire input grid to identify *all* occurrences of 2x2 squares composed *entirely* of green (3) pixels.
2.  **Record Square Locations:** Store the top-left coordinates (row, column) of each identified 2x2 green square in a list.
3.  **Transform Squares:** Iterate through the list of recorded square locations. For *each* location:
    *   Change the color of the pixel at the top-left coordinate to azure (8).
    *   Change the color of the pixel to the right of the top-left coordinate to azure (8).
    *   Change the color of the pixel below the top-left coordinate to azure (8).
    *   Change the color of the pixel diagonally down and to the right of the top-left coordinate to azure (8).
4. **Output:** Return the modified grid where identified 2x2 green squares have been changed to azure, and all other pixels remain unchanged.
"""

import numpy as np

def find_2x2_green_squares(grid):
    """Finds the top-left coordinates of all 2x2 green squares in the grid."""
    squares = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == 3 and
                grid[r, c + 1] == 3 and
                grid[r + 1, c] == 3 and
                grid[r + 1, c + 1] == 3):
                squares.append((r, c))
    return squares

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all 2x2 green squares
    squares = find_2x2_green_squares(input_grid)

    # Transform all pixels within each identified square to azure (8)
    for r, c in squares:
        output_grid[r:r+2, c:c+2] = 8

    return output_grid
```