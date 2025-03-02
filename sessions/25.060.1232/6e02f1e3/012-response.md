# 6e02f1e3 • 012 • refine_coder

---
```python
"""
Iterate through each cell of the input grid. For each cell, examine its eight 
immediate neighbors (including diagonals). Count the number of these neighbors 
that have a color different from the current cell. If this count is two or 
more, set the corresponding cell in the output grid to gray. Otherwise, set 
the corresponding cell to white.
"""

import numpy as np

def get_all_neighbors(grid, row, col):
    # Helper function to get the colors of all eight adjacent neighbors
    rows, cols = grid.shape
    neighbors = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i != 0 or j != 0) and 0 <= row + i < rows and 0 <= col + j < cols:
                neighbors.append(grid[row + i, col + j])
    return neighbors

def transform(input_grid):
    # Initialize output_grid with the same dimensions, filled with white (0)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through each cell of the input_grid
    for row in range(rows):
        for col in range(cols):
            # Get the colors of all eight neighbors
            neighbors = get_all_neighbors(input_grid, row, col)
            
            # Count the number of neighbors with different colors
            current_color = input_grid[row, col]
            different_color_count = 0
            for neighbor_color in neighbors:
                if neighbor_color != current_color:
                    different_color_count += 1

            # Apply the transformation rule
            if different_color_count >= 2:
                output_grid[row, col] = 5  # Set to gray (5)
            else:
                output_grid[row, col] = 0  # Set to white (0)

    return output_grid
```

