# d406998b • 018 • refine_coder

---
```python
"""
1.  **Initialization:** Begin with the input grid. The output grid will have the same dimensions.
2.  **White Pixel Transformation:** Examine each pixel in the input grid. If a pixel is white (0) and is adjacent (horizontally, vertically, or diagonally) to *at least* one other white (0) pixel, change its color to green (3) in the output grid.
3.  **Gray Pixel Preservation:** If a pixel is gray (5), it remains unchanged in the output grid.
4.  **Other colors:** Other colors do not appear in this task.
5. **Copy:** All other pixels that were not changed in the previous steps, copy from input to output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    output_grid = np.copy(input_grid)  # Initialize with a copy of the input
    rows, cols = input_grid.shape

    def is_adjacent_to_white(r, c, grid):
        """Checks if a cell at (r, c) is adjacent to any white pixel."""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the cell itself
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                    return True
        return False

    # Iterate and apply transformation rules
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0:  # White pixel
                if is_adjacent_to_white(r, c, input_grid):
                    output_grid[r][c] = 3  # Change to green
            # Gray pixels are implicitly handled by copying the input initially

    return output_grid
```

