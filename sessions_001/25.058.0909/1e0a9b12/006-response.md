# 3-1e0a9b12 • 006 • refine_coder

---
```python
"""
1.  **Identify and Extract:** Find all pixels in the input grid that are not zero (white). Record the color of each non-zero pixel, and keep track of the order in which you find them (reading the grid from top to bottom, and left to right).

2.  **Create Output Grid:** Make a new grid, the same size as the input grid, and fill it entirely with zeros (white).

3.  **Rearrange:** Take the non-zero pixels you found in step 1, and one by one, place them into the output grid. Start placing them at the very bottom-right corner. Fill each row from right to left. Once a row is full, move to the row above, and continue filling from right to left.

4.  **Implicit Fill:** Because the output grid starts filled with zeros, any remaining empty spaces will naturally be white (zero).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    non_zero_pixels = []

    # 1. Identify and Extract non-zero pixels (top-to-bottom, left-to-right)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append((input_grid[r, c], (r, c)))

    # 2. Create Output Grid (already done during initialization)

    # 3. Rearrange: Position non-zero pixels to bottom-right (preserving order)
    pixel_index = 0
    for r in range(rows - 1, -1, -1):  # Start at bottom row
        for c in range(cols - 1, -1, -1):  # Start at rightmost col
            if pixel_index < len(non_zero_pixels):
                output_grid[r, c] = non_zero_pixels[pixel_index][0]
                pixel_index += 1

    return output_grid.tolist()
```
