# 0ca9ddb6 • 012 • refine_coder

---
```python
"""
Transforms an input grid based on the following rules:
1. Identify non-white pixels.
2. Azure (8) pixels remain unchanged.
3. Green (3) pixels remain unchanged.
4. Blue (1) pixels generate an adjacent cross of orange (7) pixels, centered on the blue pixel.
5. Red (2) pixels generate a cross of yellow (4) pixels two spaces away, not centered on the red pixel.
6. All other cells remain or become white (0).
"""

import numpy as np

def get_non_white_pixels(grid):
    """Finds the positions and colors of all non-white pixels in the grid."""
    non_white_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                non_white_pixels.append(((r, c), grid[r, c]))
    return non_white_pixels

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.zeros_like(input_grid)
    non_white_pixels = get_non_white_pixels(input_grid)

    for (row, col), color in non_white_pixels:
        # Azure pixel remains unchanged
        if color == 8:
            output_grid[row, col] = 8
            continue

        # Green pixels remain unchanged
        if color == 3:
            output_grid[row, col] = 3
            continue

        # Handle blue pixels (create orange cross)
        if color == 1:
            output_grid[row, col] = 1  # Keep original blue pixel
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Adjacent positions
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                    output_grid[new_row, new_col] = 7

        # Handle red pixels (create yellow cross two spaces away)
        if color == 2:
            output_grid[row, col] = 2    # Keep the original red
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:  # Two spaces away
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                    output_grid[new_row, new_col] = 4

    return output_grid
```
