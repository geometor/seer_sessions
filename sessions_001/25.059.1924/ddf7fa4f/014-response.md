# ddf7fa4f • 014 • refine_coder

---
```python
"""
1.  **Reference Row:** The first row of the input grid is the reference row.
2.  **Identify Blocks:** In all rows *except* the first row, identify contiguous blocks of pixels that share the same color. A contiguous block consists of one or more pixels of the same color that are adjacent horizontally or vertically. Black (0) pixels are ignored.
3.  **Map to Reference:** Each block identified in step 2 is now considered.
4.  **Horizontal Overlap for Correspondence**: For any given block located below the reference row, compare the column range the block occupies with the reference row values at those columns. The color of the block will be changed to match the non-zero values in the reference row, if and only if, there is overlap. If there are multiple overlapping non-zero values in the reference row, any of the values can be chosen.
5.  **Replace:** Every pixel within the identified block is replaced with the determined reference color (only if a non-zero color could be identified).
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
                    if block: # Avoid empty blocks
                      blocks.append((color, block))
    return blocks

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Reference Row
    reference_row = input_grid[0]

    # 2. Identify Blocks
    blocks = find_blocks(input_grid)

    # 3. & 4. Map and Replace with Horizontal Overlap
    for color, block in blocks:
        # Find the column range of the block
        block_cols = [c for r, c in block]
        min_col = min(block_cols)
        max_col = max(block_cols)

        # Find overlapping colors in the reference row
        overlapping_colors = []
        for c in range(min_col, max_col + 1):
            if reference_row[c] != 0:
                overlapping_colors.append(reference_row[c])

        # 5. Replace if a non-zero overlapping color exists
        if overlapping_colors:
            # Choose any of the overlapping colors (here, we take the first)
            replacement_color = overlapping_colors[0]
            for row, col in block:
                output_grid[row, col] = replacement_color

    return output_grid
```
