# 234bbc79 • 014 • refine_coder

---
```python
"""
1.  **Initialization:** Create a copy of the input grid called `output_grid`. Create another copy called `white_grid`.
2.  **Remove Gray:** In both `output_grid` and `white_grid`, locate all gray (value 5) pixels and set their value to 0 (white).
3.  **Identify Expansion Zones:** `white_grid` now represents valid expansion locations, and will not change.
4.  **Identify Blue Pixels:** Find all blue pixels (value 1) in the *original* `input_grid`.
5.  **Expand Blue:** For each blue pixel in the *original* `input_grid`:
    *   Expand it within `output_grid` both horizontally and vertically.
    *   The expansion continues as long as:
        *   The new (x, y) position is within the bounds of the grid.
        *   The (x,y) location in `white_grid` is white (0).
6.  **Other Colors:** Pixels of colors other than blue or gray remain unchanged in `output_grid`.
7. **Return:** The `output_grid` is the transformed grid.
"""

import numpy as np
from collections import deque

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def expand_blue(output_grid, white_grid, start_x, start_y):
    """Expands the blue pixel from (start_x, start_y) to fill connected 0s, constrained by white_grid."""
    queue = deque([(start_x, start_y)])
    while queue:
        x, y = queue.popleft()
        if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1] and white_grid[x,y] == 0 and output_grid[x,y] != 1:
            output_grid[x, y] = 1  # Fill with blue
            # Add adjacent cells to the queue
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))


def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    # Initialize the output grid and white_grid as copies of the input grid.
    output_grid = input_grid.copy()
    white_grid = input_grid.copy()

    # Remove gray (5) pixels, converting them to white (0) in both grids.
    gray_pixels = find_pixels_by_color(input_grid, 5)
    for x, y in gray_pixels:
        output_grid[x, y] = 0
        white_grid[x, y] = 0

    # Find all blue (1) pixels in the original input grid.
    blue_pixels = find_pixels_by_color(input_grid, 1)

    # Expand each blue pixel.  Use output_grid for expansion and white_grid for constraints.
    for x, y in blue_pixels:
        expand_blue(output_grid, white_grid, x, y)

    return output_grid
```

