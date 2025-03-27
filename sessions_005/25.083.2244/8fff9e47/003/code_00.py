"""
The transformation rule involves creating a larger output grid by:
1. Mirroring the input grid vertically and stacking it with the original to form the top-left quadrant.
2. Mirroring the top-left quadrant horizontally to form the top-right quadrant.
3. Inflating each pixel of the original input grid into a rectangle of the same dimensions of the original input grid. Stacking these inflated rectangles in row major order.
4. Bottom-left quadrant is not populated and defaults to zeros.
"""

import numpy as np

def mirror_grid_vertically(grid):
    """Mirrors a grid vertically."""
    return np.flipud(grid)

def mirror_grid_horizontally(grid):
    """Mirrors a grid horizontally"""
    return np.fliplr(grid)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows, output_cols = rows * 2, cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Create mirrored copy for top-left
    mirrored_grid = mirror_grid_vertically(input_grid)

    # Stack original and mirrored to form top-left
    top_left_quadrant = np.vstack((input_grid, mirrored_grid))

    # Mirror the Top Left Quadrant and create Top Right
    top_right_quadrant = mirror_grid_horizontally(top_left_quadrant)

    # Place the top-left quadrant
    output_grid[:rows, :cols] = input_grid
    output_grid[rows:output_rows, :cols] = mirrored_grid


    # Place the top-right quadrant
    output_grid[:output_rows, cols:] = top_right_quadrant

    # Inflate and stack for bottom-right
    for i in range(rows):
      for j in range(cols):
        val = input_grid[i,j]
        for x in range(rows):
            for y in range(cols):
              output_grid[rows + x, cols + y] = val

    return output_grid