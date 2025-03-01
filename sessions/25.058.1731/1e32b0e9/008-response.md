# 1e32b0e9 • 008 • refine_coder

---
```python
"""
Identifies azure (color 8) lines and blocks in the input grid. Extends azure lines
into adjacent white (color 0) pixels. Azure blocks (more than one pixel wide in
both directions, including single pixels) remain unchanged.
"""

import numpy as np

def find_azure_elements(grid):
    """
    Finds and classifies azure elements as lines or blocks.
    Returns a list of lines and a list of blocks.
    Lines are represented as a list of (row, col) coordinates.
    Blocks are represented as a list of (row, col) coordinates.
    """
    azure_pixels = np.argwhere(grid == 8)
    lines = []
    blocks = []
    
    visited = set()

    for r, c in azure_pixels:
        if (r, c) in visited:
            continue

        element = []
        queue = [(r, c)]
        visited.add((r,c))

        while queue:
            curr_r, curr_c = queue.pop(0)
            element.append((curr_r, curr_c))

            neighbors = [(curr_r - 1, curr_c), (curr_r + 1, curr_c),
                         (curr_r, curr_c - 1), (curr_r, curr_c + 1)]

            for nr, nc in neighbors:
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] == 8 and (nr, nc) not in visited:
                    queue.append((nr, nc))
                    visited.add((nr, nc))
        
        #Classify
        is_line = True
        if len(element) > 1:
          rows, cols = zip(*element)
          min_row, max_row = min(rows), max(rows)
          min_col, max_col = min(cols), max(cols)

          if max_row - min_row > 0 and max_col - min_col > 0:
            is_line = False
        
        if is_line:
          lines.append(element)
        else:
          blocks.append(element)      

    return lines, blocks

def extend_lines(grid, lines):
    """
    Extends azure lines into adjacent white pixels.
    """
    output_grid = np.copy(grid)
    extended = True
    
    while extended:
        extended = False
        new_lines = []
        for line in lines:
          
          new_line = line.copy()
          for r, c in line:
              neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
              for nr, nc in neighbors:
                  if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and output_grid[nr, nc] == 0:
                      output_grid[nr, nc] = 8
                      if (nr,nc) not in new_line:
                        new_line.append((nr,nc))
                      extended = True
          new_lines.append(new_line)
        lines = new_lines

    return output_grid

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Find azure lines and blocks
    lines, blocks = find_azure_elements(output_grid)

    # Extend azure lines into adjacent white pixels
    output_grid = extend_lines(output_grid, lines)
    
    # blocks are implicitly preserved because extend_lines only modifies the grid
    # based on the 'lines' data

    return output_grid
```
