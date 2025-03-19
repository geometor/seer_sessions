# caa06a1f • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Regions:** Locate three distinct regions in the input grid based on color: magenta (6), orange (7), and green (3).
2.  **Remove Green Region:** Eliminate the green (3) region entirely from the grid.
3.  **Checkerboard Rearrangement:** Rearrange the remaining magenta (6) and orange (7) pixels into a checkerboard pattern, starting with orange in the top-left corner, and alternating colors in both horizontal and vertical directions. The final dimensions are the height and width of the green square combined.
"""

import numpy as np

def get_region(grid, color):
    """Finds a region of the specified color within the grid."""
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    # Identify Regions
    magenta_region = get_region(input_grid, 6)
    orange_region = get_region(input_grid, 7)
    green_region = get_region(input_grid, 3)

    # Determine dimensions of combined non-green region, assuming a perfect rectangle can be made after green is removed
    min_x = min(np.min(magenta_region[:, 1]), np.min(orange_region[:, 1]))
    max_x = max(np.max(magenta_region[:, 1]), np.max(orange_region[:, 1]))
    min_y = min(np.min(magenta_region[:, 0]), np.min(orange_region[:, 0]))
    max_y = max(np.max(magenta_region[:, 0]), np.max(orange_region[:, 0]))
    
    width = input_grid.shape[1]  # Full width from green region.
    height = input_grid.shape[0] # Full height.

    # Initialize output grid
    output_grid = np.zeros((height, width), dtype=int)

    # Checkerboard Rearrangement
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                output_grid[y, x] = 7  # Orange
            else:
                output_grid[y, x] = 6  # Magenta

    return output_grid
```
