# d07ae81c • 006 • refine_coder

---
```python
"""
1.  **Identify Special Pixels:** Determine the majority color in the input grid. Pixels that do *not* have the majority color are "special pixels."

2.  **Preserve Special Pixels:** Special pixels retain their original colors in the output grid.

3.  **Background Pixel Transformation - Simple Adjacency:**
    *   If a background pixel (majority color) is adjacent (horizontally, vertically, or diagonally) to a special pixel of color 8, change the background pixel to 8.
    *   If a background pixel is adjacent to color 1, change it to 8.
    *   If a background pixel is adjacent to color 4, change it to 8.
    *   Special pixels with colors 5 and 6 do not cause changes to neighboring background pixels.

4.  **Background Pixel Transformation - Vertical Stripes and Alternating Fill (refined):**
    *   If there are 2x2 blocks of special pixels forming vertical stripes where a column of color `C1` is immediately to the left or right of a column of color `C2`, then apply an alternating fill:

      *   If a background pixel is adjacent to `C1` it will transform to a fill color.
      *   The fill color is determined as follows:
        *   If C1 = 3 and C2 = 8, the fill color is 3.
        *   If C1 = 8 and C2 = 3, the fill color is 6.
        *   If C1 = 3 and C2 is any other color except 8, the fill color is 6

5. **Prioritization**: Simple adjacency rules take precedence. The Vertical Stripe rule applies to what remains.
"""

import numpy as np

def get_special_pixels(grid):
    """
    Identifies "special" pixels (those not of the majority color).
    """
    values, counts = np.unique(grid, return_counts=True)
    majority_color = values[np.argmax(counts)]
    special_pixels = {}
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != majority_color:
                special_pixels[(r, c)] = grid[r, c]
    return special_pixels, majority_color

def get_neighbors(grid, r, c):
    """Gets the 8 neighbors (including diagonals) of a pixel."""
    neighbors = {}
    for i in range(max(0, r - 1), min(grid.shape[0], r + 2)):
        for j in range(max(0, c - 1), min(grid.shape[1], c + 2)):
            if (i, j) != (r, c):
                neighbors[(i, j)] = grid[i, j]
    return neighbors

def is_vertically_striped(grid, special_pixels, color1, color2):
    """Checks if special pixels form vertical stripes with given colors."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r,c) in special_pixels and grid[r,c] == color1:
              if c > 0 and grid[r,c-1] == color2 and (r, c-1) in special_pixels:
                return True
              if c < grid.shape[1] -1 and grid[r,c+1] == color2 and (r, c+1) in special_pixels:
                return True
    return False

def transform(input_grid):
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    special_pixels, majority_color = get_special_pixels(grid)

    # Preserve special pixels
    for (r, c), color in special_pixels.items():
        output_grid[r, c] = color

    # Background pixel transformation - Simple Adjacency
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == majority_color:
                neighbors = get_neighbors(grid, r, c)
                neighbor_colors = list(neighbors.values())

                if 8 in neighbor_colors or 1 in neighbor_colors or 4 in neighbor_colors:
                    output_grid[r, c] = 8

    # Background Pixel Transformation - Vertical Stripes (after adjacency)
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if output_grid[r,c] == majority_color:
                if is_vertically_striped(grid, special_pixels, 3, 8):
                    if c > 0 and grid[r, c-1] == 3 and (r, c-1) in special_pixels:
                        output_grid[r, c] = 3

                elif is_vertically_striped(grid, special_pixels, 8, 3):
                    if c > 0 and grid[r,c-1] == 8 and (r, c-1) in special_pixels:
                         output_grid[r,c] = 6
                elif is_vertically_striped(grid, special_pixels, 3, 6) or is_vertically_striped(grid, special_pixels, 3, 0):  #check for other colors adjacent to color 3
                  if c > 0 and grid[r,c-1] == 3 and (r,c-1) in special_pixels:
                        output_grid[r,c] = 6
    return output_grid.tolist()
```
