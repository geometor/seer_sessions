# 09629e4f • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify the dividing line:** Locate the horizontal line of grey (5) pixels at row index 3 in the input grid.
2.  **Preserve the dividing line:** Copy the grey line from input to output.
3.  **Locate colored regions:** Scan the input grid, both above and below the dividing line. Identify 3x3 blocks of pixels where all pixels have the same color, and that color is *not* grey (5) or white (0).
4.  **Replicate the blocks:** Copy to the output those identified 3 x 3 blocks of pixels and keeping their position in respect to the separator line.
5.  **Fill remaining pixels:** In the output grid, replace all pixels that are *not* part of the dividing line or the identified 3x3 colored regions with white (0).
"""

import numpy as np

def find_3x3_blocks(grid):
    blocks = []
    height, width = grid.shape
    for i in range(height - 2):
        for j in range(width - 2):
            subgrid = grid[i:i+3, j:j+3]
            first_color = subgrid[0, 0]
            if first_color != 5 and first_color != 0 and np.all(subgrid == first_color):
                blocks.append(((i, j), first_color))
    return blocks

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Preserve the dividing line (all grey - 5)
    output_grid[3, :] = 5

    # Find 3x3 blocks
    blocks = find_3x3_blocks(input_grid)

    # Replicate blocks in output and keep separator
    for (row, col), color in blocks:
      output_grid[row:row+3, col:col+3] = color

    return output_grid
```
