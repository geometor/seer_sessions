# 77fdfe62 • 006 • refine_coder

---
```python
"""
1.  **Identify Non-White Blocks:** Examine the input grid and identify contiguous blocks of non-white pixels. A block is defined as a rectangular region of pixels of the same color.
2.  **Order Blocks:** Order the identified blocks. Ordering is done based on the position of the block within the input grid, reading the input grid in a standard raster scan (from top to bottom, and within each row, from left to right). Use the top-left pixel of a block as the block position.
3.  **Create Output Grid:** Prepare a 4x4 output grid, initially filled with white (0).
4.  **Populate Output Grid:** Fill the output grid with colors from the ordered blocks.
    *   Start at the top-left cell (0, 0) of the output grid.
    *   Iterate through the non-white blocks in order.
    *   Iterate the pixels of a block, taking the colors row by row, left to right.
    * Place the pixel color into the output grid moving from left-to-right, top-to-bottom
    *   If the output grid is full, stop populating.
    *   If all non-white pixels have been placed, complete filling the rest of the output grid with 0.
"""

import numpy as np

def find_blocks(grid):
    """Finds contiguous blocks of non-white pixels in a grid."""
    blocks = []
    visited = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                block_color = grid[r, c]
                block = []
                queue = [(r, c)]
                visited.add((r, c))
                while queue:
                    curr_r, curr_c = queue.pop(0)
                    block.append((curr_r, curr_c, block_color))
                    # Check adjacent cells (up, down, left, right)
                    neighbors = [(curr_r - 1, curr_c), (curr_r + 1, curr_c),
                                 (curr_r, curr_c - 1), (curr_r, curr_c + 1)]
                    for nr, nc in neighbors:
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == block_color and (nr, nc) not in visited:
                            queue.append((nr, nc))
                            visited.add((nr, nc))
                blocks.append(block)
    return blocks

def order_blocks(blocks):
    """Orders blocks based on the top-left pixel's position (raster-scan order)."""
    return sorted(blocks, key=lambda block: (block[0][0], block[0][1]))

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((4, 4), dtype=int)

    # Find and order blocks
    blocks = find_blocks(input_grid)
    ordered_blocks = order_blocks(blocks)

    # Populate output grid
    row, col = 0, 0
    for block in ordered_blocks:
        for r, c, color in block:
          if (row < 4):
            output_grid[row, col] = color
            col += 1
            if col >= 4:
                col = 0
                row += 1

    return output_grid
```
