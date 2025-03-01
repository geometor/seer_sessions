# 40853293 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify "seed" pixels:** Locate all single, isolated pixels of colors red, green, azure, magenta, white and gray in the input grid.
2.  **Red Extension:** For the red pixel, extend it vertically upwards, maintaining the red color, until it reaches the top edge of the grid.
3.  **Azure Extension:** For the azure pixel, extend it vertically downwards, maintaining the azure color, until it reaches the bottom edge of the grid.
4.  **Green, Magenta, White, Gray Extension:**
     - copy all pixels of these colors 6 times to the right,
     - the magenta pixel also has the gray pixels to the left and right.
"""

import numpy as np

def find_seed_pixels(grid):
    """Finds single, isolated pixels of specified colors."""
    seed_pixels = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:  # Non-background pixel
                # Check if it's isolated (not part of a larger object)
                is_isolated = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == grid[r, c]:
                            is_isolated = False
                            break
                    if not is_isolated:
                        break
                if is_isolated:
                    if grid[r,c] not in seed_pixels:
                      seed_pixels[grid[r, c]] = (r, c)
    return seed_pixels

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    seed_pixels = find_seed_pixels(input_grid)

    # Red Extension
    if 2 in seed_pixels:
        red_r, red_c = seed_pixels[2]
        for r in range(red_r):  # Up to the top
            output_grid[r, red_c] = 2

    # Azure Extension
    if 8 in seed_pixels:
        azure_r, azure_c = seed_pixels[8]
        for r in range(azure_r + 1, rows): # Down to the bottom
            output_grid[r, azure_c] = 8

    # Green, Magenta, Gray and White Extension
    colors_to_extend = [3, 6, 5, 0]
    for color in colors_to_extend:
      if color in seed_pixels:
        if color == 6: # magenta
          r, c = seed_pixels[color]
          for i in range(7):
            if c + i < cols:
              output_grid[r,c + i] = 6
          output_grid[r, c+1] = 5
          output_grid[r, c+2] = 5
          output_grid[r, c+3] = 6
          output_grid[r, c+4] = 5
          output_grid[r, c+5] = 5
          output_grid[r, c+6] = 5

        elif color==3: # green
          r, c = seed_pixels[color]
          for i in range(7):
                if c + i < cols:
                  output_grid[r,c + i] = 3
          output_grid[r,c+3]=2

        elif color==5:
          r, c = seed_pixels[color]
          for i in range(7):
                if c + i < cols:
                  output_grid[r,c + i] = 5


    return output_grid
```
