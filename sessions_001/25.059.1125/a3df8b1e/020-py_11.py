"""
1.  Identify the most prominent non-white color in the input grid, considering only pixels along the main diagonal from the top-right to the bottom-left. If there are multiple colors with the same count along the diagonal, prioritize in this order: gray, then blue, then green, then other colors.
2.  Draw a diagonal line from the top-right corner to the bottom-left corner of the grid.
3.  Set the color of this diagonal line to the prominent color identified in step 1.
4. If the prominent color was present as a single pixel, and that color is blue, then replace the original blue single pixel with a white pixel.
"""

import numpy as np

def get_prominent_diagonal_color(grid):
    """Identifies the most prominent non-white color along the main diagonal (top-right to bottom-left)."""
    rows, cols = grid.shape
    diagonal_colors = []
    for r in range(rows):
        for c in range(cols):
            if r == rows - 1 - c:
                if grid[r, c] != 0:  # Exclude white
                    diagonal_colors.append(grid[r, c])

    if not diagonal_colors:
        return 0  # Return white if no non-white colors on the diagonal

    counts = {}
    for color in diagonal_colors:
        counts[color] = counts.get(color, 0) + 1

    # Find the most frequent color
    max_count = 0
    prominent_color = 0
    for color, count in counts.items():
      if count > max_count:
          max_count = count
          prominent_color = color
      elif count == max_count:
        if prominent_color == 0:
          prominent_color = color
        elif color == 5: # gray priority
          prominent_color = color
        elif color == 1 and prominent_color != 5: # blue
          prominent_color = color
        elif color == 3 and prominent_color != 5 and prominent_color != 1: # green
          prominent_color = color

    return prominent_color

def find_single_pixel(grid):
    """Finds the coordinates of single-colored pixels in the grid."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    single_pixels = []

    for color in unique_colors:
        if np.sum(grid == color) == 1:
            row, col = np.where(grid == color)
            single_pixels.append((row[0], col[0], color))
            
    return single_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify the most prominent non-white color on the diagonal.
    prominent_color = get_prominent_diagonal_color(input_grid)

    # 2. & 3. Draw the diagonal line with the prominent color.
    for r in range(rows):
        for c in range(cols):
            if r == rows - 1 - c:
                output_grid[r, c] = prominent_color

    # 4. Replace single blue pixel with white
    single_pixels = find_single_pixel(input_grid)
    for r, c, color in single_pixels:
      if color == 1:
        output_grid[r,c] = 0


    return output_grid