```python
"""
The input grid contains one or more colored (non-black) pixels. These pixels are replicated in the output grid, maintaining their original color. The replication follows a specific pattern: the original pixel position is maintained, and a second copy is placed halfway across the output grid horizontally. If the output grid is taller than wide, additional copies are made below the originals. Azure (8) pixels are added to fill in a specific pattern, primarily in the even-numbered rows and columns, forming a border-like structure. The output grid's dimensions are double the input grid's dimensions.
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
    # Find the colored pixels in the input grid.
    colored_pixels = find_colored_pixels(input_grid)

    # Initialize the output grid with double the dimensions of the input grid.
    out_rows = len(input_grid) * 2
    out_cols = len(input_grid[0]) * 2
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # Replicate the colored pixels.
    for r, c, color in colored_pixels:
        # Original position
        output_grid[r, c] = color

        # Replicated position (halfway across horizontally)
        new_c = c + out_cols // 2
        if new_c < out_cols:
            output_grid[r, new_c] = color
        
        #Additional copies if output is taller
        row_offset = len(input_grid)
        new_r = r + row_offset
        while new_r < out_rows:
            output_grid[new_r,c] = color
            if new_c < out_cols:
                output_grid[new_r, new_c] = color
            new_r += row_offset


    # Add Azure border.
    for r in range(out_rows):
        for c in range(out_cols):
          if output_grid[r,c] == 0:  # Fill only empty cells.
              if r % 2 == 0 and c % 2 == 0:
                output_grid[r, c] = 8

    return output_grid
```