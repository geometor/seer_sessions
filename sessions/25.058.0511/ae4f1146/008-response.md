# ae4f1146 • 008 • example_2 • investigate_coder

---
```python
"""
Extracts a 3x3 subgrid from the input grid. The subgrid is defined as the 
top-right-most contiguous block of 1s (blue) and 8s (azure).
"""

import numpy as np

def find_contiguous_blocks(grid, colors):
    """
    Finds all contiguous blocks of specified colors in the grid.
    Returns a list of lists, where each inner list contains the (row, col) coordinates
    of a contiguous block.
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    blocks = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, block):
        visited.add((r, c))
        block.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and (nr, nc) not in visited and grid[nr][nc] in colors:
                dfs(nr, nc, block)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in colors and (r, c) not in visited:
                block = []
                dfs(r, c, block)
                blocks.append(block)
    return blocks

def top_rightmost_block(blocks):
   """Finds the block whose top-right corner is furthest to the right, then top.

    Args:
        blocks: list of lists
   """
   if not blocks:
       return []

   # sort the block by col then row in decending order
   top_rightmost = sorted(blocks, key=lambda block: (max(c for _, c in block), -min(r for r, _ in block)), reverse = True)
   return top_rightmost[0]

def transform(input_grid):
    """
    Extracts the top-right-most 3x3 subgrid of contiguous 1s and 8s.
    """
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find all contiguous blocks of 1s and 8s
    blocks = find_contiguous_blocks(grid, [1, 8])

    #find the right most block
    target_block = top_rightmost_block(blocks)

    if not target_block:
        return None # return None for empty cases
    
    # Determine top-right corner coordinates of this block
    max_col = max(c for _, c in target_block)
    min_row = min(r for r, _ in target_block)
    
    # Adjust the top-right corner if it is on the border of the grid, so that a complete 3 x 3 can be formed
    tr_row = min_row
    tr_col = max_col
    
    if tr_row > (grid.shape[0] - 3):
      tr_row = grid.shape[0] - 3

    if tr_col < 2:
      tr_col = 2
    
    # Extract the 3x3 subgrid
    output_grid = grid[tr_row:tr_row + 3, tr_col - 2:tr_col + 1].tolist()
    
    return output_grid
```
