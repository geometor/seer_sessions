```python
"""
1.  **Identify Background:** The background color is azure (8).
2.  **Find Isolated Pixels:** Iterate through all pixels in the input grid. A pixel is considered "isolated" if *all* of its immediate neighbors (up, down, left, right, and diagonals) have the background color (azure).
3. **Change color:** Isolated pixels that do not have the background color are changed to green (3).
4.  **Preserve Non-Isolated:** Pixels that are not isolated are not changed.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 3x3 neighborhood around a pixel."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def is_isolated(grid, row, col, background_color=8):
    """Checks if a pixel is surrounded by the background color."""
    neighbors = get_neighbors(grid, row, col)
    return all(neighbor == background_color for neighbor in neighbors)

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Identify Background: The background color is azure (8).
    background_color = 8

    # Find Isolated Pixels and change their color
    for i in range(rows):
        for j in range(cols):
            #Check if the pixel is isolated and not the background
            if output_grid[i,j] != background_color and is_isolated(output_grid, i, j, background_color):
                output_grid[i,j] = 3

    return output_grid.tolist()
```