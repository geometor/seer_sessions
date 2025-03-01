# ba26e723 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** all contiguous blocks of yellow (4) pixels in the input grid.
2.  **For each yellow block**:
    *   If a yellow pixel is on a corner of a block replace the yellow pixel with a magenta (6) pixel. Corners are left and right ends of a horizontal block.
    *    If a yellow pixel borders a white pixel on any edge on the left or right, replace that yellow pixel with a magenta (6).
3.  **Retain** all white (0) pixels in their original positions.
4.  **Output** the modified grid.
"""

import numpy as np

def find_yellow_blocks(grid):
    # Find contiguous blocks of yellow pixels
    yellow_blocks = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_block):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != 4:
            return
        visited.add((r, c))
        current_block.append((r, c))
        dfs(r + 1, c, current_block)
        dfs(r - 1, c, current_block)
        dfs(r, c + 1, current_block)
        dfs(r, c - 1, current_block)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 4 and (r, c) not in visited:
                current_block = []
                dfs(r, c, current_block)
                yellow_blocks.append(current_block)
    return yellow_blocks

def transform(input_grid):
    output_grid = np.copy(input_grid)
    yellow_blocks = find_yellow_blocks(input_grid)

    for block in yellow_blocks:
      #find horizontal blocks
      rows = [p[0] for p in block]
      cols = [p[1] for p in block]
      if len(set(rows)) == 1: #horizontal block identified

        #replace corners/ends with magenta
        min_col = min(cols)
        max_col = max(cols)
        output_grid[rows[0],min_col] = 6
        output_grid[rows[0],max_col] = 6
      
      #check for left and right bordering white
      for r,c in block:
        if c > 0 and input_grid[r,c-1] == 0:
          output_grid[r,c] = 6
        if c < input_grid.shape[1]-1 and input_grid[r,c+1] == 0:
          output_grid[r,c] = 6

    return output_grid
```
