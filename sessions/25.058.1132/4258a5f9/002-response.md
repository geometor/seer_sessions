# 4258a5f9 • 002 • example_2 • investigate_coder

---
```python
"""
1. Identify Gray Pixels: Locate all pixels in the input grid with the value 5 (gray).
2. Surround with Blue: For each gray pixel, change the color of all its 8-connected neighboring pixels (including diagonals) to 1 (blue). If a neighbor is already gray (5), do not change it.
3. Gray Pixels Unchanged: gray pixels retain their original location and color
4. Output Grid: The resulting grid after applying these changes is the output.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 8-connected neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the cell itself
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Find the coordinates of all gray pixels (value 5)
    gray_pixels = np.argwhere(input_grid == 5)


    # Iterate through each gray pixel
    for row, col in gray_pixels:
        # Get the 8-connected neighbors of the current gray pixel
        neighbors = get_neighbors(input_grid, row, col)

        # Change the color of neighboring pixels to blue (1) if they aren't gray
        for r, c in neighbors:
            if output_grid[r, c] != 5:  # Check if the neighbor is not gray
                output_grid[r, c] = 1

    return output_grid
```
