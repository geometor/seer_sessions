# 28bf18c6 • 019 • refine_coder

---
```python
"""
The transformation rule depends on how many colors are in the grid:

1.  **Single Non-Zero Color:** If the input grid contains only one non-zero color, extract the bounding box of all pixels of that color.
2.  **Multiple Non-Zero Colors:** If the input grid contains multiple non-zero colors, extract a *single pixel* of each of those colors. The output pixels should be arranged vertically in the order that the color appears in the input rows. The relative row order of the extracted pixels reflects the row order in which the colors first appear in the input.
"""

import numpy as np

def get_bounding_box(grid, color):
    """
    Finds the bounding box of a specific color in a grid.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return (0, 0, 0, 0)  # Handle cases with no pixels of the color
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def extract_single_pixels(input_grid):
    """
    Extracts a single pixel of each non-zero color, preserving row order.
    """
    input_grid = np.array(input_grid)
    non_zero_colors = np.unique(input_grid[input_grid != 0])
    output_grid = []
    color_rows = {} # keep track of first row

    for color in non_zero_colors:
       rows, cols = np.where(input_grid == color)
       color_rows[color] = np.min(rows) # keep first row

    # order colors by row
    sorted_colors = sorted(non_zero_colors, key=lambda color: color_rows[color])
    for color in sorted_colors:
        output_grid.append([color])


    return output_grid


def transform(input_grid):
    """
    Transforms the input grid based on the number of unique colors.
    """
    input_grid = np.array(input_grid)
    non_zero_colors = np.unique(input_grid[input_grid != 0])

    if len(non_zero_colors) == 1:
        # Single non-zero color: bounding box
        color = non_zero_colors[0]
        min_row, max_row, min_col, max_col = get_bounding_box(input_grid, color)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        output_grid = np.zeros((height, width), dtype=int)
        for r in range(height):
            for c in range(width):
                if input_grid[min_row + r, min_col + c] == color:
                    output_grid[r, c] = color
        return output_grid.tolist()

    else:
        # Multiple non-zero colors: extract single pixels
      
        return extract_single_pixels(input_grid)
```
