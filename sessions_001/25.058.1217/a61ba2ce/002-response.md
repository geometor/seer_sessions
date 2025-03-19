# a61ba2ce • 002 • example_2 • investigate_coder

---
```python
"""
Extracts colored blocks from a large input grid, removes surrounding empty space, and places them into a smaller 4x4 output grid, maintaining their relative positions and order of appearance.
"""

import numpy as np

def get_colored_blocks(grid):
    """Identifies and extracts colored blocks from the input grid."""
    blocks = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, block_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        block_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, block_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                block_coords = []
                dfs(r, c, color, block_coords)
                # Find top-left and bottom-right for bounding box
                min_r = min(coord[0] for coord in block_coords)
                min_c = min(coord[1] for coord in block_coords)
                max_r = max(coord[0] for coord in block_coords)
                max_c = max(coord[1] for coord in block_coords)

                blocks.append({
                    'color': color,
                    'top_left': (min_r, min_c),
                    'shape' : (max_r - min_r + 1, max_c - min_c + 1),
                    'coords': block_coords
                })
    return blocks

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Identify colored blocks
    blocks = get_colored_blocks(input_grid)

    # Initialize output grid (4x4)
    output_grid = np.zeros((4, 4), dtype=int)

    # Place blocks into output grid
    row_offset = 0
    col_offset = 0

    for block in blocks:
       for r_delta in range(block['shape'][0]):
          for c_delta in range(block['shape'][1]):
            if row_offset + r_delta < 4 and col_offset + c_delta < 4:
                output_grid[row_offset+r_delta, col_offset+c_delta] = block['color']

       col_offset += block['shape'][1]
       if col_offset >= 4:
          col_offset = 0
          row_offset += 2


    return output_grid
```
