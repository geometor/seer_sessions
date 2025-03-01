"""
1.  **Identify Rectangles:** Locate horizontal rectangular blocks of uniform color within the input grid.
2.  **Target Middle Row:** For each identified rectangle, focus on its middle row.
3.  **Poke Checkerboard:** Within the middle row of each rectangle, alternate the existing color with white (0), starting with the original color and then 0, until the end of the block on that row.
4. **Keep the rest** Keep all pixels outside the colored rectangles, and any part of a color other than the middle line, as is.
"""

import numpy as np

def find_rectangles(grid):
    # Find contiguous horizontal blocks of the same color
    rectangles = []
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
                    rectangles.append(((r, start_col), (r, c - 1), current_color))
                start_col = c
                current_color = grid[r, c]
        if start_col is not None and current_color !=0:
             rectangles.append(((r, start_col), (r, cols-1), current_color))
    return rectangles

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find rectangles
    rectangles = find_rectangles(input_grid)

    # Iterate through rectangles and poke holes in the middle row
    for rect in rectangles:
      start,end, color = rect
      start_row, start_col = start
      end_row, end_col = end
      
      height = end_row - start_row +1
      if height > 1 :
        mid_row = start_row + height // 2

        # Poke holes
        for c in range(start_col, end_col + 1):
            if (c - start_col) % 2 == 1:
                output_grid[mid_row, c] = 0


    return output_grid