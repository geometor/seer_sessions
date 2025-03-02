"""
Transforms an input grid containing isolated green (3) and azure (8) pixels by:

1. Expanding each green and azure pixel into a 3x3 block of the same color, centered on the original pixel's location.
2. Connecting the *nearest* expanded blocks of different colors (green and azure) with a horizontal path of grey (5) pixels.  The path starts from the right edge of the green block and extends to the left edge of the azure block. If the blocks overlap horizontally, no connection is made.
3. The connection path lies on the row that is the vertical center of the green block.
4. All other pixels are white (0).
"""

import numpy as np

def find_pixels(grid, color_value):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color_value).tolist()

def expand_pixel(grid, coord, color_value):
    """Expands a pixel into a 3x3 block centered at the given coordinate."""
    rows, cols = grid.shape
    r, c = coord
    for i in range(max(0, r - 1), min(rows, r + 2)):
        for j in range(max(0, c - 1), min(cols, c + 2)):
            grid[i, j] = color_value

def connect_blocks(grid, green_coord, azure_coord):
    """
    Connects two expanded blocks (3x3) with a horizontal grey (5) path.
    The path goes from the right edge of the green block to the left edge of the azure block.
    The path is on the center row of the green block.
    """
    green_center_row = green_coord[0]
    green_right_col = green_coord[1] + 1
    azure_left_col = azure_coord[1] - 1

    if green_right_col <= azure_left_col:
        for c in range(green_right_col, azure_left_col + 1):
            grid[green_center_row, c] = 5


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.zeros_like(input_grid)
    
    # 1. Find initial pixels
    green_pixels = find_pixels(input_grid, 3)
    azure_pixels = find_pixels(input_grid, 8)

    # 2. Expand Pixels
    for pixel in green_pixels:
      expand_pixel(output_grid, pixel, 3)
    for pixel in azure_pixels:
      expand_pixel(output_grid, pixel, 8)

    # 3. Connect the nearest blocks with grey pixels.
    for g_pixel in green_pixels:
      min_dist = float('inf')
      nearest_a_pixel = None
      for a_pixel in azure_pixels:
          dist = abs(g_pixel[1] - a_pixel[1]) + abs(g_pixel[0]-a_pixel[0]) # Manhattan distance
          if dist < min_dist:
              min_dist = dist
              nearest_a_pixel = a_pixel

      if nearest_a_pixel is not None:
          connect_blocks(output_grid, g_pixel, nearest_a_pixel)

    return output_grid