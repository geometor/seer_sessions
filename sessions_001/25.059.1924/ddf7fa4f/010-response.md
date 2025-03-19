# ddf7fa4f • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify Reference Colors:** Observe the colors and their positions in the first row of the input grid. These are the "reference colors."
2.  **Locate Target Blocks:** Identify the contiguous blocks of color 'gray', 'yellow', and 'orange' in the rest of the grid.
3. **Map Input to Output** For the given input, gray (5) is mapped to blue(1), yellow(4) maps to yellow (4), and orange (7) maps to orange (7). The colors, blue (1), yellow (4), and orange (7) correspond to the reference color on the top row of the input.
4.  **Replace Colors:** For each block below the top row, replace all the pixels with the value, matching the reference colors on the top row of the input grid.
"""

import numpy as np

def find_blocks(grid):
    """
    Finds contiguous blocks of the same color in the grid, excluding the top row.
    """
    blocks = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, block):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        block.append((r, c))
        dfs(r + 1, c, color, block)
        dfs(r - 1, c, color, block)
        dfs(r, c + 1, color, block)
        dfs(r, c - 1, color, block)

    for r in range(1, rows):  # Start from the second row
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0:
                    block = []
                    dfs(r, c, color, block)
                    blocks.append((color, block))
    return blocks

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Reference Colors
    reference_colors = {}
    for c in range(cols):
        color = input_grid[0, c]
        if color != 0:
            reference_colors[c] = color

    # 2. Locate Target Blocks (excluding the top row)
    blocks = find_blocks(input_grid)

    # 3 & 4. Map and Replace Colors
    
    for color, block in blocks:
      first_coord = block[0]
      r = first_coord[0]
      c = first_coord[1]

      if color == 5:
        replace = 1
      elif color == 4:
        replace = 4
      elif color == 7:
        replace = 7
      else:
        # default is don't change value
        replace = color
      for row, col in block:
          output_grid[row, col] = replace

    return output_grid
```
