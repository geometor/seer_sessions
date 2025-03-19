# 1f85a75f • 014 • refine_coder

---
```python
"""
The transformation identifies the longest horizontal line of a single color, other than white (0), that is adjacent to a different color. It then extracts a segment of that line, starting one pixel after the intersection and extending for a length determined by the extent of the secondary color.

"""

import numpy as np

def find_longest_horizontal_line(grid):
    """Finds the longest horizontal line of a non-zero color."""
    rows, cols = grid.shape
    longest_line = []
    current_line = []

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0:
                current_line.append((row, col))
            else:
                if len(current_line) > len(longest_line):
                    longest_line = current_line
                current_line = []
        if len(current_line) > len(longest_line):
            longest_line = current_line
        current_line = []  # Reset for the next row
    return longest_line

def find_adjacent_color_extent(grid, row, col, direction):
    """
    Finds the extent of a different color adjacent to a given position.
    Direction: 1 for right, -1 for left.
    """
    rows, cols = grid.shape
    original_color = grid[row, col]
    extent = 0
    col += direction

    while 0 <= col < cols and grid[row, col] != original_color and grid[row,col] != 0:
        extent += 1
        col += direction

    return extent

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Find the longest horizontal line (of non-zero color)
    longest_line = find_longest_horizontal_line(input_grid)
    
    if not longest_line:
      return [[]]

    #initialize the output grid
    output_grid = np.empty((0,0))

    # Iterate through the line to find intersections with other colors
    for row, col in longest_line:
      color = input_grid[row,col]
      
      # Check right neighbor
      if col + 1 < cols and input_grid[row, col + 1] != color and input_grid[row,col+1] != 0:
          extent = find_adjacent_color_extent(input_grid, row, col, 1)
          start_col = col+2 #start after intersection
          end_col = min(cols, start_col + extent)
          
          output_grid = np.array([[input_grid[row,c] for c in range(start_col,end_col)]])
          if output_grid.size > 0: #check valid output
            return output_grid.tolist()
          

      # Check left neighbor
      if col - 1 >= 0 and input_grid[row, col - 1] != color and input_grid[row, col -1] != 0:
          extent = find_adjacent_color_extent(input_grid, row, col, -1)
          start_col = col - 1 -1 #one before intersection
          end_col = max(-1,start_col-extent)

          output_grid = np.array([[input_grid[row,c] for c in range(start_col,end_col, -1)]])
          if output_grid.size > 0:
              return output_grid.tolist()

    return [[]]  # Default: empty output
```
