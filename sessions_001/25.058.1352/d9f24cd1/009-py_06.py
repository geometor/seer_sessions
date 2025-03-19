"""
Red pixels expand to fill adjacent cells, constrained by gray pixels.
"""

import numpy as np

def get_adjacent_pixels(grid, r, c):
    """
    Get the valid adjacent pixels for a given cell.
    """
    rows, cols = grid.shape
    adjacent = []
    if r > 0:
        adjacent.append((r - 1, c))  # Up
    if r < rows - 1:
        adjacent.append((r + 1, c))  # Down
    if c > 0:
        adjacent.append((r, c - 1))  # Left
    if c < cols - 1:
        adjacent.append((r, c + 1))  # Right
    return adjacent

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Find initial red pixels
    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 2:
                red_pixels.append((r, c))

    # Expand red pixels (flood fill)
    pixels_to_fill = red_pixels.copy()
    filled_pixels = set()

    while pixels_to_fill:
        current_pixel = pixels_to_fill.pop()
        r, c = current_pixel

        if current_pixel in filled_pixels:
            continue
        filled_pixels.add(current_pixel)

        if output_grid[r,c] != 5:
          output_grid[r, c] = 2  # Fill current pixel with red if not gray

          # Add adjacent pixels to the queue if not gray
          for ar, ac in get_adjacent_pixels(output_grid, r, c):
              if output_grid[ar, ac] != 5 and (ar,ac) not in filled_pixels:
                  pixels_to_fill.append((ar, ac))

    return output_grid