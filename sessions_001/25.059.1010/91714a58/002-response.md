# 91714a58 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to find the largest, solid-colored, rectangular, contiguous block within the input grid and preserve it in the output grid, setting all other pixels to white (0).
"""

import numpy as np

def find_largest_block(grid):
    """
    Finds the largest contiguous block of the same color in the grid.
    Returns a tuple: (color, (start_row, start_col), (end_row, end_col)) of the largest block.
    Returns (None, None, None) if the grid is empty or no blocks are found.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_size = 0
    max_block = (None, None, None)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_block):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_block.append((r, c))

        dfs(r + 1, c, color, current_block)
        dfs(r - 1, c, color, current_block)
        dfs(r, c + 1, color, current_block)
        dfs(r, c - 1, color, current_block)


    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r,c] != 0:
                current_block = []
                dfs(r, c, grid[r, c], current_block)
                
                if current_block:
                    min_row = min(cell[0] for cell in current_block)
                    max_row = max(cell[0] for cell in current_block)
                    min_col = min(cell[1] for cell in current_block)
                    max_col = max(cell[1] for cell in current_block)
                    
                    #check if the shape is rect
                    block_size = (max_row - min_row + 1) * (max_col - min_col + 1)
                    if block_size == len(current_block):
                        if block_size > max_size:
                            max_size = block_size
                            max_block = (grid[r, c], (min_row, min_col), (max_row, max_col))

    return max_block

def transform(input_grid):
    """
    Transforms the input grid by preserving the largest solid-colored rectangular block
    and setting all other pixels to 0.
    """
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    
    # Initialize output_grid with all zeros, same size as input
    output_grid = np.zeros_like(input_grid)

    # Find the largest block
    color, start_coords, end_coords = find_largest_block(input_grid)

    # If a block is found, copy it to the output grid
    if color is not None:
        start_row, start_col = start_coords
        end_row, end_col = end_coords
        output_grid[start_row:end_row+1, start_col:end_col+1] = color

    return output_grid.tolist()
```
