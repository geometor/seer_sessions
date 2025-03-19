# aba27056 • 020 • refine_coder

---
```python
"""
1.  **Identify Source and Target:** The input grid contains *source pixels* (green) and *target pixels* (white).
2.  **Propagate Yellow to Adjacent cells:** For each *target pixel* (white), check if it's directly adjacent (horizontally, vertically, or diagonally) to a *source pixel* (green).
3.  **Change Target based on source adjancency:** If a *target pixel* is adjacent to a *source_pixel*, change the *target_pixel* to yellow.
4. **No other Changes:** Source Pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))  # Store coordinates, not just values
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the input grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is a target pixel (white)
            if input_grid[row, col] == 0:
                # Get the neighbors of the current pixel
                neighbors = get_neighbors(input_grid, row, col)
                # Check if any of the neighbors are source pixels (green)
                for neighbor_row, neighbor_col in neighbors:
                    if input_grid[neighbor_row, neighbor_col] == 3:
                        # If a neighbor is green, change the current pixel to yellow
                        output_grid[row, col] = 4
                        break  # No need to check other neighbors once one is found

    return output_grid
```

