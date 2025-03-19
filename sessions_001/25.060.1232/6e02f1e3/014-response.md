# 6e02f1e3 • 014 • refine_coder

---
```python
"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid, initially filled entirely with white pixels (color 0).

2.  **Gray Pixel Retention:** Iterate through each pixel of the *input* grid.
    *   If a pixel is gray (color 5) *and* all of its eight immediate neighbors (horizontal, vertical, and diagonal) are white (color 0), then set the corresponding pixel in the *output* grid to gray (color 5).

3.  **Default to White:** All other input pixels do not change the output grid - they remain white.
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
            # Check if the current pixel is gray
            if input_grid[row, col] == 5:
                # Get the colors of all eight neighbors
                neighbors = get_all_neighbors(input_grid, row, col)
                
                # Check if all neighbors are white
                all_white = True
                for neighbor_color in neighbors:
                    if neighbor_color != 0:
                        all_white = False
                        break
                
                # If all neighbors are white, set the corresponding output pixel to gray
                if all_white:
                    output_grid[row, col] = 5

    return output_grid
```
