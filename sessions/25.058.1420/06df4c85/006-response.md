# 06df4c85 • 006 • refine_coder

---
```python
"""
The transformation rule identifies 2x2 blocks of uniform color within the input grid. If a 2x2 block is red or green, it's horizontally expanded by duplicating it once to its right. Blue 2x2 blocks and the background (white) remain unchanged. The output grid is dynamically sized to accommodate the expansions.
"""

import numpy as np

def find_2x2_blocks(grid):
    """Finds all 2x2 blocks of the same color and returns their top-left coordinates and color."""
    blocks = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            color = grid[r, c]
            if (grid[r:r+2, c:c+2] == color).all():
                blocks.append((r, c, color))
    return blocks

def calculate_output_size(input_grid):
    """Calculates the output grid size based on the number of red/green 2x2 blocks."""
    blocks = find_2x2_blocks(input_grid)
    rows, cols = input_grid.shape
    additional_cols = 0
    for r, c, color in blocks:
        if color == 2 or color == 3:  # Red or Green
            additional_cols += 2
    return rows, cols + additional_cols

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    rows, cols = input_grid.shape
    out_rows, out_cols = calculate_output_size(input_grid)
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # Find 2x2 blocks
    blocks = find_2x2_blocks(input_grid)

    # Create a mapping from original column index to output column index
    col_map = {}
    output_col = 0
    for input_col in range(cols):
        col_map[input_col] = output_col
        output_col += 1

    # Adjust column mapping for expansions
    for r, c, color in blocks:
      if color == 2 or color == 3:
        for i in range(c + 1, cols):
          col_map[i] += 2

    # Copy and expand
    for r in range(rows):
        for c in range(cols):
            output_grid[r, col_map[c]] = input_grid[r, c]
            
    for r, c, color in blocks:
        if color == 2 or color == 3:  # Red or Green
          output_grid[r:r+2, col_map[c]+2:col_map[c]+4] = input_grid[r:r+2,c:c+2]

    return output_grid
```
