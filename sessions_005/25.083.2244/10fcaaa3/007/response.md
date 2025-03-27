```python
"""
1. Double Grid Size: Create an output grid with dimensions double that of the input grid (twice the rows and twice the columns).

2. Identify Colored Pixels: Find all pixels in the input grid that are not black (0). Note their coordinates (row, column) and color value.

3. Replicate Colored Pixels: For each colored pixel:
    *   Copy the pixel to the same position in the output grid.
    *   Copy the pixel to a second location in the output grid. This second location is horizontally offset by half the width of the *output* grid.

4. Vertical Replication (Conditional):
   - if output grid is taller than wide, replicate color pixels vertically by
     input.height

5. Add Azure Border: Iterate through every cell of the output grid.
    - if the cell is empty (value is 0)
      - Fill it with azure (8) under these conditions:
        - If the current column index is even, then if the row is even, fill
        - If the current column index is odd, don't fill the current cell.
"""

import numpy as np

def find_colored_pixels(grid):
    # Find the coordinates and color of all non-black pixels.
    coords = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                coords.append((r, c, value))
    return coords

def transform(input_grid):
    # Double Grid Size
    out_rows = len(input_grid) * 2
    out_cols = len(input_grid[0]) * 2
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # Identify Colored Pixels
    colored_pixels = find_colored_pixels(input_grid)

    # Replicate Colored Pixels
    for r, c, color in colored_pixels:
        # Original position
        output_grid[r, c] = color

        # Horizontal Replication
        new_c = c + out_cols // 2
        if new_c < out_cols:
          output_grid[r, new_c] = color

        # Vertical Replication
        row_offset = len(input_grid)
        new_r = r + row_offset
        while new_r < out_rows:
          output_grid[new_r,c] = color
          if new_c < out_cols:
            output_grid[new_r,new_c] = color
          new_r += row_offset

    # Add Azure Border
    for r in range(out_rows):
        for c in range(out_cols):
            if output_grid[r, c] == 0:  # Check if the cell is empty
                if c % 2 == 0: # if col is even
                    if r % 2 == 0: # if row is even
                        output_grid[r, c] = 8


    return output_grid
```