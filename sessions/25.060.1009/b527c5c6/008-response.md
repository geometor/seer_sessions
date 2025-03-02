# b527c5c6 • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate the green (3) "cross" shape and the red (2) pixel within it.

2.  **Red Pixel Duplication:** For each red (2) pixel in the input, create four copies in the output: one directly above, one directly below, one to the left, and one to the right. Place these copies only on white (0) pixels.

3.  **Green Cross Horizontal Expansion:** Extend the arms of the green (3) cross horizontally.  For each green pixel on the cross, examine the pixels to its immediate left and right. If a neighboring pixel is white (0), change it to green (3).

4.  **Green Cross Vertical Expansion:** After horizontal expansion, extend the green cross *only to match the existing height of the original green pixels*. Scan upwards and downwards *from the original green cross only*, changing any white (0) pixels to green (3) until another color, including newly created green, is encountered.
"""

import numpy as np

def get_objects(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify red pixels
    red_pixels = get_objects(input_grid, 2)
    
    # Duplicate red pixels (Step 2)
    for r, c in red_pixels:
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 0:
                output_grid[nr, nc] = 2

    # Identify original green pixels (Step 1 & 3)
    original_green_pixels = get_objects(input_grid, 3)
    min_row, max_row = rows, -1
    for r, c in original_green_pixels:
        min_row = min(min_row,r)
        max_row = max(max_row,r)
    
    # Horizontal Expansion of Green Cross (Step 3)
    for r, c in original_green_pixels:
        if c > 0 and input_grid[r,c-1] == 0: #Check original grid
            output_grid[r,c-1] = 3
        if c < cols -1 and input_grid[r, c+1] == 0: # Check original grid
            output_grid[r, c+1] = 3
            
    # Vertical Fill for original green pixels (Step 4)
    for r, c in original_green_pixels:
        # Upwards
        for ur in range(r - 1, min_row-1, -1):
            if output_grid[ur, c] == 0:
                output_grid[ur, c] = 3
            else:
                break
        # Downwards
        for dr in range(r + 1, max_row + 1):
            if output_grid[dr, c] == 0:
                output_grid[dr, c] = 3
            else:
                break

    return output_grid
```
