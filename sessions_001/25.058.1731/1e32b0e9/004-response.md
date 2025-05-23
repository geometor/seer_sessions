# 1e32b0e9 • 004 • example_1 • investigate_coder

---
```python
"""
Extends blue pixels horizontally and/or vertically to adjacent azure pixels.
"""

import numpy as np

def find_lines(grid, color):
    lines = []
    rows, cols = grid.shape

    # Find horizontal lines
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                line_start = c
                while c < cols and grid[r, c] == color:
                    c += 1
                line_end = c - 1
                if line_end > line_start:
                    lines.append(((r, line_start), (r, line_end), 'horizontal'))
                c -=1 #important!

    # Find vertical lines
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == color:
                line_start = r
                while r < rows and grid[r, c] == color:
                    r += 1
                line_end = r - 1
                if line_end > line_start:
                     lines.append(((line_start, c), (line_end, c), 'vertical'))
                r -= 1 #important

    return lines

def extend_lines(grid, lines):
    
    output_grid = np.copy(grid)
    
    extended = True
    while extended:
      extended = False
      for line in lines:
          start, end, direction = line
          
          if direction == 'horizontal':
              r, c_start = start
              r_end, c_end = end
  
              # Extend left
              if c_start > 0 and output_grid[r, c_start - 1] == 0:
                  output_grid[r, c_start - 1] = 8
                  lines.append(  ((r,c_start - 1), (r,c_start - 1), 'horizontal' ) )
                  extended = True

              
              # Extend right
              if c_end < output_grid.shape[1] - 1 and output_grid[r, c_end + 1] == 0:
                  output_grid[r, c_end + 1] = 8
                  lines.append(  ((r,c_end+1), (r,c_end+1), 'horizontal' ) )
                  extended = True
  
          elif direction == 'vertical':
              r_start, c = start
              r_end, c_end = end
  
              # Extend up
              if r_start > 0 and output_grid[r_start - 1, c] == 0:
                  output_grid[r_start - 1, c] = 8
                  lines.append( ((r_start-1, c), (r_start-1,c), 'vertical') )
                  extended = True
              
              # Extend down
              if r_end < output_grid.shape[0] - 1 and output_grid[r_end + 1, c] == 0:
                  output_grid[r_end + 1, c] = 8
                  lines.append(  ((r_end+1,c), (r_end+1,c), 'vertical' ) )
                  
                  extended = True

    return output_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find blue lines
    blue_lines = find_lines(output_grid, 8)
    
    #extend the lines
    output_grid = extend_lines(output_grid, blue_lines)

    return output_grid
```
