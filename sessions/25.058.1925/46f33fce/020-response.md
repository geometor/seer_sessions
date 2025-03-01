# 46f33fce • 020 • refine_coder

---
```python
"""
Transforms the input grid by identifying colored pixels, doubling the grid
dimensions, and then replicating each colored pixel four times, arranging them
in a 2x2 grid within the output grid. The relative positions of colors in the
input determines output quadrant positions.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies each non-zero pixel as a separate object, keyed by color.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A dictionary where keys are colors and values are lists of (row, col)
        tuples representing the object's pixels.  Each pixel is its own object.
    """
    objects = {}
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != 0:
                if color not in objects:
                    objects[color] = []
                objects[color].append((r, c))
    return objects

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2, input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # find objects in input grid (each pixel is an object)
    objects = find_objects(input_grid)

    # sort colors by input position (top-to-bottom, then left-to-right)
    sorted_colors = sorted(objects.keys(), key=lambda color: objects[color][0])

    # replicate and arrange objects (colored pixels)
    for color in sorted_colors:
        # use first coordinate for the color to calculate output positions
        r, c = objects[color][0]
        output_grid[r, c] = color
        output_grid[r, c + input_cols] = color
        output_grid[r + input_rows, c] = color
        output_grid[r + input_rows, c + input_cols] = color

    return output_grid
```
