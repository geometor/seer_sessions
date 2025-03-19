# d406998b • 004 • refine_coder

---
```python
"""
1.  **Identify Regions:** Find all contiguous regions of gray (5) pixels and white (0) pixels in the input grid.
2.  **Check Adjacency:** For each pixel in a gray region, check its immediate neighbors (up, down, left, right).
3.  **Transform Gray Pixels:** If a gray pixel is directly adjacent to at least two white (0) pixels, change that pixel to green (3).
4. Copy all white pixels to the output
5. All other colors remain unchanged
"""

import numpy as np

def count_adjacent_whites(grid, row, col):
    """Counts the number of white (0) adjacent pixels to a given cell."""
    rows, cols = grid.shape
    count = 0
    # Check up
    if row > 0 and grid[row-1, col] == 0:
        count += 1
    # Check down
    if row < rows - 1 and grid[row+1, col] == 0:
        count += 1
    # Check left
    if col > 0 and grid[row, col-1] == 0:
        count += 1
    # Check right
    if col < cols - 1 and grid[row, col+1] == 0:
        count += 1
    return count

def transform(input_grid):
    # Initialize output grid with the same dimensions and data type as the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # If the pixel is gray (5)
            if input_grid[row, col] == 5:
                # Count adjacent white pixels
                white_count = count_adjacent_whites(input_grid, row, col)
                # If at least two adjacent pixels are white, change to green (3)
                if white_count >= 2:
                    output_grid[row, col] = 3
            # else the output grid already has the correct value from the np.copy

    return output_grid
```
