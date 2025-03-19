# 9d9215db • 020 • refine_coder

---
```python
"""
1. Identify Source Pixels: Locate all non-zero pixels in the input grid. These are the "source pixels."
2. Create and remove Block (except source): For each source pixel, temporarily create a 3x3 block of the same color centered on the source pixel. Remove the block, but keep the original source pixel intact.
3. Horizontal Extension: For each source pixel, extend a horizontal line of the same color to the left and right edges of the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Source Pixels
    source_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                source_pixels.append((r, c, input_grid[r, c]))

    # 2 & 3. Iterate through source pixels
    for r, c, color in source_pixels:
        # Create 3x3 block (temporarily)
        min_row = max(0, r - 1)
        max_row = min(rows, r + 2)
        min_col = max(0, c - 1)
        max_col = min(cols, c + 2)

        for block_r in range(min_row, max_row):
            for block_c in range(min_col, max_col):
                output_grid[block_r, block_c] = color
        
        # Remove block except for source
        for block_r in range(min_row, max_row):
            for block_c in range(min_col, max_col):
                if (block_r, block_c) != (r,c):
                    output_grid[block_r, block_c] = 0


        # Horizontal Extension
        output_grid[r, :] = color  # Set entire row to the color

    return output_grid
```

