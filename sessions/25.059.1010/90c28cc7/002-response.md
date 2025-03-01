# 90c28cc7 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation identifies the distinct color blocks in the input grid and represents them on x,y grid in the output grid, the output grid represent the position of the first occurrence (top,left) of each different color.
"""

import numpy as np

def find_blocks(grid):
    """
    Identifies distinct rectangular blocks of color in the grid.
    """
    blocks = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, block):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        block.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, block)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0:  # Ignore background color
                    block = []
                    dfs(r, c, color, block)
                    blocks.append( (color,block) )
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by representing distinct color blocks.
    """
    # Find distinct blocks in the input grid
    blocks = find_blocks(np.array(input_grid))

    # Extract unique colors and their top-left positions
    color_positions = []
    
    for color,pixels in blocks:
      min_row = min(p[0] for p in pixels)
      min_col = min(p[1] for p in pixels)
      color_positions.append( (color, (min_row,min_col)))
      
    
    # Sort by row and then by column
    color_positions.sort(key=lambda item: (item[1][0], item[1][1]))

    
    # Determine dimensions and initialize output
    n_colors = len(color_positions)
    
    max_rows = 0
    
    current_row = -1
    row_count = -1
    colors_per_row = []
    
    for i in range(len(color_positions)):
      if color_positions[i][1][0] > current_row:
        current_row = color_positions[i][1][0]
        row_count+=1
        colors_per_row.append(0)
      
      colors_per_row[row_count]+=1
      
    max_rows = len(colors_per_row)
    max_cols = max(colors_per_row)
    
    
    output_grid = np.zeros((max_rows, max_cols), dtype=int)

    # Populate output grid with representative colors
    current_row = -1
    current_col = -1
    row_count = -1
    
    for color, pos in color_positions:
        if pos[0] > current_row:
            current_row = pos[0]
            row_count += 1
            current_col = 0
        else:
            current_col += 1
        output_grid[row_count, current_col] = color

    return output_grid.tolist()
```
