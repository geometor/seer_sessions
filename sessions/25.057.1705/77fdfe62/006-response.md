# 77fdfe62 • 006 • refine_coder

---
```python
"""
The transformation removes a surrounding blue border and white background pixels. The remaining pixels, which form a distinct inner figure, are condensed into a smaller grid. The relative positions of the pixels within the inner figure are preserved during the condensation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing the blue border and white background,
    then condensing the remaining pixels into a smaller output grid, preserving relative positions.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify and Remove Border: Remove blue (1) border pixels.
    def remove_blue_border(grid):
        rows, cols = grid.shape
        if rows <= 2 or cols <= 2:  # Nothing to remove if too small
            return grid

        # Check if the outer layer is all blue
        if (np.all(grid[0, :] == 1) and np.all(grid[rows - 1, :] == 1) and
            np.all(grid[:, 0] == 1) and np.all(grid[:, cols - 1] == 1)):

            return grid[1:rows-1, 1:cols-1] #remove border
        return grid

    grid_no_border = remove_blue_border(input_grid)

    # 2. & 3. Identify, Remove Background, and Extract Inner Figure
    def extract_inner_figure(grid):
        rows, cols = grid.shape
        inner_pixels = []
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] != 0 and grid[r,c] != 1: #not white or blue
                    inner_pixels.append((r, c, grid[r, c]))
        return inner_pixels

    inner_figure = extract_inner_figure(grid_no_border)

    # 4. Determine the arrangement and size of output
    def get_output_dimensions(inner_figure):
       if not inner_figure:
          return 0,0

       rows = [p[0] for p in inner_figure]
       cols = [p[1] for p in inner_figure]

       min_row, max_row = min(rows), max(rows)
       min_col, max_col = min(cols), max(cols)

       return max_row - min_row + 1, max_col - min_col + 1

    output_rows, output_cols = get_output_dimensions(inner_figure)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    #5. Condense and preserve, populate the output grid
    if inner_figure:
       min_row = min([p[0] for p in inner_figure])
       min_col = min([p[1] for p in inner_figure])
       for r, c, color in inner_figure:
            output_grid[r - min_row, c - min_col] = color

    return output_grid
```
