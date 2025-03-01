# e73095fd • 015 • refine_coder

---
```python
"""
1.  **Identify the Gray Shape:** Find the contiguous block of gray (5) pixels. This forms the main object.
2.  **Find Outer Corners:** Within the gray shape, identify the "outer corner" pixels. An outer corner is defined as a gray pixel that has exactly two adjacent gray neighbors, and these two neighbors are also adjacent to each other (either horizontally or vertically). Diagonal neighbors are not considered for corner identification.
3. **Change Corners to Yellow:** Change color of identified corner pixels from gray (5) to yellow (4).
4. **Output:** The output grid is the same as the input grid, except with the identified corner pixels changed to yellow.
"""

import numpy as np

def find_gray_shape(grid):
    # Find all gray pixels
    gray_pixels = np.argwhere(grid == 5)
    return gray_pixels

def is_outer_corner(grid, row, col):
    # Check if a gray pixel is an outer corner
    gray = 5

    if grid[row, col] != gray:
        return False

    # Count adjacent neighbors (horizontal/vertical only)
    neighbors = 0
    neighbor_coords = []
    if row > 0 and grid[row-1, col] == gray:
        neighbors += 1
        neighbor_coords.append((row - 1, col))
    if row < grid.shape[0] - 1 and grid[row + 1, col] == gray:
        neighbors += 1
        neighbor_coords.append((row + 1, col))
    if col > 0 and grid[row, col - 1] == gray:
        neighbors += 1
        neighbor_coords.append((row, col - 1))
    if col < grid.shape[1] - 1 and grid[row, col + 1] == gray:
        neighbors += 1
        neighbor_coords.append((row, col + 1))

    # Check if it's an outer corner (exactly two neighbors, and they are adjacent)
    if neighbors == 2:
        row1, col1 = neighbor_coords[0]
        row2, col2 = neighbor_coords[1]
        if (abs(row1 - row2) == 1 and col1 == col2) or \
           (abs(col1 - col2) == 1 and row1 == row2):
            return True

    return False

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find gray shape pixels
    gray_pixels = find_gray_shape(input_grid)

    # Iterate and find outer corner locations, replace them with yellow
    for row, col in gray_pixels:
        if is_outer_corner(output_grid, row, col):
            output_grid[row, col] = 4

    return output_grid
```
