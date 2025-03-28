```python
"""
Identifies two red (2) marker pixels in the input grid. If exactly two markers are found and they are aligned horizontally, vertically, or diagonally, it modifies the pixels located strictly between these markers. White (0) pixels between the markers are changed to red (2), and blue (1) pixels between the markers are changed to green (3). All other pixels, including the markers themselves, remain unchanged. If there are not exactly two red markers, or if they are not aligned, the grid is returned unmodified.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels with the specified color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find red marker pixels
    red_markers = find_pixels_by_color(input_grid, 2)

    # Check if exactly two red markers exist
    if len(red_markers) != 2:
        return output_grid # Return unmodified grid if not exactly two markers

    (r1, c1), (r2, c2) = red_markers

    # Determine alignment and iterate between markers
    if r1 == r2: # Horizontal alignment
        start_col = min(c1, c2) + 1
        end_col = max(c1, c2)
        for c in range(start_col, end_col):
            if input_grid[r1, c] == 0:
                output_grid[r1, c] = 2
            elif input_grid[r1, c] == 1:
                output_grid[r1, c] = 3
    elif c1 == c2: # Vertical alignment
        start_row = min(r1, r2) + 1
        end_row = max(r1, r2)
        for r in range(start_row, end_row):
            if input_grid[r, c1] == 0:
                output_grid[r, c1] = 2
            elif input_grid[r, c1] == 1:
                output_grid[r, c1] = 3
    elif abs(r1 - r2) == abs(c1 - c2): # Diagonal alignment
        # Determine direction
        dr = 1 if r2 > r1 else -1
        dc = 1 if c2 > c1 else -1

        # Iterate between points (excluding endpoints)
        curr_r, curr_c = r1 + dr, c1 + dc
        while (curr_r, curr_c) != (r2, c2):
             # Check bounds just in case, though logic should prevent out-of-bounds
            if 0 <= curr_r < height and 0 <= curr_c < width:
                if input_grid[curr_r, curr_c] == 0:
                    output_grid[curr_r, curr_c] = 2
                elif input_grid[curr_r, curr_c] == 1:
                    output_grid[curr_r, curr_c] = 3
            curr_r += dr
            curr_c += dc
    # If not aligned, no changes are made beyond the initial copy

    return output_grid
```