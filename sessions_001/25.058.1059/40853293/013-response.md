# 40853293 • 013 • refine_coder

---
```python
"""
1.  **Identify Yellow Pixels:** Locate all pixels with a value of 4 (yellow).

2.  **Vertical Expansion (Yellow):** For each yellow pixel, extend its color (4) downwards in its column. Stop when either the bottom edge of the grid is reached, or a pixel with a value other than 0 (background) or 4 (yellow) is encountered.

3.  **Horizontal Expansion and Fill (Other Colors):** For each row, perform the following:

    *   Check for the presence of both yellow pixels (4) and at least one other non-background pixel (not 0) with a different color.
    *   If both conditions are met, find the leftmost and rightmost non-background pixels in that row.
    *   Fill all background pixels (0) between the leftmost and rightmost non-background pixels with the color of the non-yellow, non-background pixel found in that row. If there are more than one non-yellow colors on a row, they act as 'stoppers' and independently cause filling from their side.
"""

import numpy as np

def get_yellow_pixels(grid):
    """Finds the coordinates of all yellow (4) pixels."""
    yellow_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 4:
                yellow_pixels.append((r, c))
    return yellow_pixels

def expand_vertically(grid, start_row, col):
    """Expands yellow (4) pixels downwards until another object or edge."""
    rows = grid.shape[0]
    current_row = start_row

    while current_row < rows:
        if grid[current_row,col] != 0 and grid[current_row,col] !=4:
            break
        grid[current_row, col] = 4
        current_row += 1

def expand_horizontally_and_fill(grid):
    """Expands colored pixels horizontally in rows occupied by expanded yellow."""
    rows = grid.shape[0]
    cols = grid.shape[1]

    for r in range(rows):
        # Find non-background pixels
        non_background_pixels = []
        for c in range(cols):
            if grid[r, c] != 0:
                non_background_pixels.append((r, c))

        # Check if both yellow and other colors exist in the row
        has_yellow = any(grid[r, c] == 4 for _, c in non_background_pixels)
        other_colors = any(grid[r, c] != 4 for _, c in non_background_pixels)

        if has_yellow and other_colors:
            # Find leftmost and rightmost non-background pixel indices
            non_yellow_pixels = [(row,col) for (row,col) in non_background_pixels if grid[row,col] != 4]

            for (row,col) in non_yellow_pixels:
                fill_color = grid[row,col]

                # fill to the left
                current_col = col - 1
                while current_col >= 0 and grid[r,current_col] == 0:
                    grid[r,current_col] = fill_color
                    current_col -= 1
                # fill to the right
                current_col = col + 1
                while current_col < cols and grid[r,current_col] == 0:
                    grid[r,current_col] = fill_color
                    current_col += 1


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find yellow pixel coordinates
    yellow_pixels = get_yellow_pixels(output_grid)

    # expand the yellow pixels vertically
    for r, c in yellow_pixels:
        expand_vertically(output_grid, r, c)

    # expand other colored pixels horizontally and fill
    expand_horizontally_and_fill(output_grid)

    return output_grid
```
