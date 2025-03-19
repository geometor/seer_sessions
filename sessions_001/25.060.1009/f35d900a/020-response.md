# f35d900a • 020 • refine_coder

---
```python
"""
1.  **Identify Red and Yellow Pixels:** Locate all pixels with values 2 (red) and 4 (yellow) in the input grid.
2.  **Expand Red and Yellow:** For *each* red and yellow pixel:
    *   If the red/yellow pixel shares a row with *another* red or yellow pixel (but not the same column), expand it vertically into a 3x1 rectangle (centered on the original pixel).
    *   If the red/yellow pixel shares a column with *another* red or yellow pixel (but not the same row), expand it horizontally into a 1x3 rectangle (centered on the original pixel).
    *   If the red/yellow pixel shares *both* a row and a column with *another* red or yellow pixel, expand it into a 3x3 square (centered on the original pixel).
    *    If none of the above applies, keep the pixel with its color.
3.  **Handle Intersections:** Where the expanded regions of red and yellow pixels overlap, change the overlapping pixels to gray (value 5).
4. **Preserve Background:** All other pixels retain their original input color (which will mostly be white).
5.  **Output Grid:** Create the output grid by initializing with the background color and apply the expansion and intersection actions to update only the cells affected by the transformation.
"""

import numpy as np

def get_colored_pixels(grid, color):
    """Finds coordinates of pixels of a specific color."""
    return np.argwhere(grid == color)

def expand_pixel(grid, coord, color):
    """Expands a pixel based on other red/yellow neighbors."""
    row, col = coord
    height, width = grid.shape
    output_grid = np.copy(grid)  # Work on a copy

    # Find other red/yellow pixels
    other_colored_pixels = get_colored_pixels(grid, 2)
    other_colored_pixels = np.concatenate((other_colored_pixels,get_colored_pixels(grid,4)))

    other_colored_pixels = other_colored_pixels[~np.all(other_colored_pixels == coord, axis=1)] #remove the current pixel


    has_colored_neighbor_row = False
    has_colored_neighbor_col = False

    for other_row, other_col in other_colored_pixels:
        if other_row == row and other_col != col:
            has_colored_neighbor_row = True
        if other_col == col and other_row != row:
            has_colored_neighbor_col = True

    if has_colored_neighbor_row and has_colored_neighbor_col:
        # Expand to 3x3
        for i in range(max(0, row - 1), min(height, row + 2)):
            for j in range(max(0, col - 1), min(width, col + 2)):
                output_grid[i, j] = color
    elif has_colored_neighbor_row:
        # Expand vertically (3x1)
        for i in range(max(0, row - 1), min(height, row + 2)):
            output_grid[i, col] = color
    elif has_colored_neighbor_col:
        # Expand horizontally (1x3)
        for j in range(max(0, col - 1), min(width, col + 2)):
            output_grid[row, j] = color
    else:
      output_grid[row,col]=color


    return output_grid

def handle_intersections(grid):
    """Places gray pixels at intersections of expanded red and yellow regions."""
    output_grid = np.copy(grid)
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
          if grid[r,c] == 2:
            for r2 in range(height):
              for c2 in range(width):
                if grid[r2,c2] == 4:
                  if (r == r2 and abs(c-c2) <= 2) or (c == c2 and abs(r-r2)<=2) or (abs(r-r2)<=2 and abs(c-c2)<=2):
                      output_grid[r,c] = 5
                      output_grid[r2,c2] = 5

    return output_grid


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Initialize output grid with a copy of the input_grid
    output_grid = np.copy(input_grid)

    red_pixels = get_colored_pixels(input_grid, 2)
    yellow_pixels = get_colored_pixels(input_grid, 4)

    # Expand red pixels, modifying the output_grid
    for coord in red_pixels:
      output_grid = expand_pixel(output_grid, coord, 2)

    # Expand yellow pixels, modifying the output_grid
    for coord in yellow_pixels:
        output_grid = expand_pixel(output_grid, coord, 4)

    # Handle intersections
    output_grid = handle_intersections(output_grid)

    return output_grid
```
