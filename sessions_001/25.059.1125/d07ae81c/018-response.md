# d07ae81c • 018 • example_3 • investigate_coder

---
```python
"""
The transformation identifies a central blue stripe in the input grid, then mirrors/shifts and recolors parts of it in the output grid. Some blue (1) pixels become green (3) or azure (8), with special chaotic rules for azure (8). Green pixels are preserved, and highlighted. The center column (8) preserves some original color structure.
"""

import numpy as np

def find_central_stripe(grid):
    """Finds the central vertical stripe of blue (1) pixels."""
    height, width = grid.shape
    center_col = width // 2
    stripe_cols = []

    # Check for blue(1) in the center columns
    for col_offset in range(-1,2):
        if all(grid[:, center_col+col_offset] == 1):
             stripe_cols.append(center_col + col_offset)
        
    return stripe_cols

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = input_grid.copy()
    height, width = input_grid.shape
    stripe_cols = find_central_stripe(input_grid)

    # Iterate through the grid
    for r in range(height):
        for c in range(width):
            # Handle central stripe mirroring and recoloring
            if c in stripe_cols:
                # implement stripe recoloring (blue to green or azure)
                if input_grid[r,c] == 1:

                    # Recolour to green, azure (somewhat pseudo-random for now - based on input pattern)
                    if (r+c) % 5 == 0:
                        output_grid[r,c] = 3 # Green
                    if (r+c) % 7 == 0:
                        output_grid[r, c] = 8 # Azure

                continue  #skip to next pixel
            # mirroring of central column across columns
            dist_to_center = abs(c - width // 2)

            if dist_to_center>0 and dist_to_center <= len(stripe_cols):
                # find mirrored color position
                mirrored_col = width // 2 + (width//2 - c)
                if mirrored_col < width and mirrored_col >= 0 :

                    new_val = input_grid[r,mirrored_col]

                    if input_grid[r, c] == 1:
                        if new_val != 8 and (r+c) % 4 == 0 :
                            output_grid[r,c] = 3
                        if new_val == 8 and (r+c) % 3 == 0:
                            output_grid[r,c] = 8

                    # chaotic downward movement
                    if input_grid[r, c] == 1:
                        if r+1<height :
                            if input_grid[r+1, c] != 8:
                                if (r*c)% 5 == 0:
                                    output_grid[r+1,c] = 3
                            if input_grid[r+1, c] == 8:
                                if (r+c)% 3 == 0:
                                    output_grid[r+1, c] = 8
            # Preserve Green
            if input_grid[r,c] == 3:

                # do something to highlight the isolated nature, surround

                if c>0 and output_grid[r, c-1] != 3:
                    output_grid[r, c-1] = 6
                if c+1 < width and output_grid[r, c+1] !=3:
                    output_grid[r, c+1] = 6



    return output_grid
```
