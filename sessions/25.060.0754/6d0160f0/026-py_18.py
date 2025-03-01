"""
1.  **Identify Separators:** Locate all pixels with the color gray (5).
2.  **Preserve Separators:** Maintain the gray pixels in their original positions in the output grid.
3.  Within the two horizontal gray lines, locate the positions of any colors in the top most segment
4.  If any color exists in that segment between two vertical gray lines, maintain the first occurence of each unique non zero color just below the horizontal divider
5.  **Replace other colors:** Replace all other colored pixels that do not meet the previous condition with white color (0).
"""

import numpy as np

def find_gray_separators(grid):
    """Finds the row and column indices of gray (5) pixels."""
    gray_pixels = np.where(grid == 5)
    return gray_pixels[0], gray_pixels[1]

def get_segment_colors(grid, row_start, row_end, col_start, col_end):
  """Extracts the colors present within a specific grid segment"""
  segment_colors = {}
  for r in range(row_start, row_end):
    for c in range(col_start, col_end):
      color = grid[r,c]
      if color != 0 and color != 5:
        if color not in segment_colors:
          segment_colors[color] = (r, c) #store the first location
  return segment_colors


def transform(input_grid):
    # Initialize output grid with the same dimensions and all zeros.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find gray separator positions.
    gray_rows, gray_cols = find_gray_separators(input_grid)

    # Preserve gray separators in the output grid.
    for r, c in zip(gray_rows, gray_cols):
        output_grid[r, c] = 5

    # Find the boundaries of the topmost segment
    horizontal_separators = sorted(list(set(gray_rows)))
    vertical_separators = sorted(list(set(gray_cols)))

    top_row_start = 0
    top_row_end = horizontal_separators[0]

     # Iterate through segments defined by vertical separators
    for i in range(len(vertical_separators) - 1):
        col_start = vertical_separators[i] + 1
        col_end = vertical_separators[i+1]

         # Get colors and their first positions within the topmost segment
        top_segment_colors = get_segment_colors(input_grid, top_row_start, top_row_end, col_start, col_end)

        # Determine the destination row just below the first horizontal separator
        dest_row = horizontal_separators[0] + 1

        #Place the found colors to below the gray line
        for color, (orig_r, orig_c) in top_segment_colors.items():
          #only move if its between these two vertical separators
          if col_start <= orig_c < col_end:
            output_grid[dest_row,orig_c] = color

    return output_grid