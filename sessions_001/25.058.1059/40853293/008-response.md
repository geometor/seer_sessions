# 40853293 • 008 • refine_coder

---
```python
"""
1.  **Identify Seed Pixels:** Find all pixels of colors red, azure, magenta, gray, green, and white that do *not* have a neighbor of the same color, including diagonals.  These are the "seed pixels."
2.  **Red Extension:** If a seed red pixel is found, extend it vertically upwards to the top edge of the grid.
3.  **Azure Extension:** If a seed azure pixel is found, extend it vertically downwards to the bottom edge of the grid.
4.  **Magenta Extension:** If a seed magenta pixel exists, extend it by *one* pixel horizontally in *both* directions (left and right).
5.  **Gray Extension:** If a seed gray pixel is found, extend it down to the bottom edge of the grid.
6. **Green Extension:** If a seed green pixel if found, extend it by *two* pixels to the right.
7.  **White Extension:** If a seed white pixel if found, extend it to the right by *six* pixels.
8.  If a pixel is targeted for multiple extensions, the extension associated with the color that appears first in the following list takes precedence: red, azure, magenta, gray, green, white. (This rule is added as we cannot determine the behavior for now).
"""

import numpy as np

def find_seed_pixels(grid):
    """Finds seed pixels of specified colors (no neighbors of same color, including diagonals)."""
    seed_pixels = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:  # Non-background
                is_seed = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color:
                            is_seed = False
                            break
                    if not is_seed:
                        break
                if is_seed:
                    if color not in seed_pixels:
                        seed_pixels[color] = (r,c)
    return seed_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find seed pixels
    seed_pixels = find_seed_pixels(input_grid)

    # Apply extensions based on color precedence
    color_order = [2, 8, 6, 5, 3, 0]  # Red, Azure, Magenta, Gray, Green, White

    for color in color_order:
        if color in seed_pixels:
            r, c = seed_pixels[color]

            if color == 2:  # Red
                for i in range(r):
                    output_grid[i, c] = 2
            elif color == 8:  # Azure
                for i in range(r + 1, rows):
                    output_grid[i, c] = 8
            elif color == 6:  # Magenta
                if c - 1 >= 0:
                    output_grid[r, c - 1] = 6
                if c + 1 < cols:
                    output_grid[r, c + 1] = 6
            elif color == 5:  # Gray
                for i in range(r + 1, rows):
                    output_grid[i, c] = 5
            elif color == 3: # Green
                for i in range(1,3):
                    if c + i < cols:
                        output_grid[r, c+i] = 3
            elif color == 0: # White
                for i in range(1,7):
                    if c + i < cols:
                        output_grid[r, c+i] = 0

    return output_grid
```
