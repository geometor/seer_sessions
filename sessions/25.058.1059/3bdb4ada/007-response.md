# 3bdb4ada • 007 • refine_coder

---
```python
"""
1. Identify Horizontal Lines: Find all horizontal lines of contiguous pixels of the same color (excluding white/0). Consider these as rectangles of height 1 or the center row of a rectangle of height > 1.
2. Poke Holes: For each identified horizontal line, iterate through its pixels. Set the pixel to white (0) if its position is odd relative to the starting column of the line/rectangle.
"""

import numpy as np

def find_horizontal_lines(grid):
    # Find contiguous horizontal blocks of the same color
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = None
        current_color = None
        for c in range(cols):
            if start_col is None:
                start_col = c
                current_color = grid[r, c]
            elif grid[r, c] != current_color:
                if current_color != 0:  # Ignore white background
                    lines.append(((r, start_col), (r, c - 1), current_color))
                start_col = c
                current_color = grid[r, c]
        if start_col is not None and current_color !=0:
             lines.append(((r, start_col), (r, cols-1), current_color))
    return lines

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find horizontal lines (rectangles)
    lines = find_horizontal_lines(input_grid)

    # Iterate through lines and poke holes
    for line in lines:
      start,end, color = line
      start_row, start_col = start
      end_row, end_col = end

      # Poke holes
      for c in range(start_col, end_col + 1):
          if (c - start_col) % 2 == 0: # every other, starting at start_col
              output_grid[start_row, c] = 0

    return output_grid
```
