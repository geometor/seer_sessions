"""
1.  **Identify Source Pixels:** Identify all non-zero pixels in the input grid. These are the "source" pixels.
2.  **Iterate by color, then by pixel:** loop through all of the non-zero colors, for each color loop through the source pixels.
3.  **Horizontal Extension:** For each color, create a horizontal extension to the left and right.
    *   extend one cell at a time
    *   if a color is present at the cell location, check if the color matches the current color.
        *  If colors match, stop extension
        *  If colors do not match, continue to next cell
4.  **Vertical Extension**
    *  For colors 1 (blue), 2(red), 3 (green), 4 (yellow), and 8 (azure) repeat the horizontal extension vertically.
        *   Use the same rules as the horizontal extension
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by extending non-zero pixels diagonally."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Source Pixels and 2. Iterate by Color
    unique_colors = np.unique(input_grid)
    for color in unique_colors:
        if color == 0:
            continue

        # Iterate through each source pixel of the current color
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] == color:

                    # 3. Horizontal Extension
                    output_grid[r,:] = horizontal_extend(input_grid, r, c, color)

                    # 4. Vertical Extension (only for specified colors)
                    if color in [1, 2, 3, 4, 8]:
                      for i in range(rows):
                        output_grid[i,:] = horizontal_extend(output_grid, i, c, color)


    return output_grid


def horizontal_extend(grid, row, col, color):
  rows, cols = grid.shape
  new_row = np.copy(grid[row,:])

  # extend right
  for c in range(cols):
      if c < col:
          continue
      if c == col:
          continue

      if grid[row,c] == 0:
        new_row[c] = color
      elif grid[row,c] == color:
        break # stop if colors match
      else:
          continue # continue to next if colors don't match

  # extend left
  for c in range(cols):
      cc = cols - 1 - c
      if cc > col:
          continue
      if cc == col:
        continue
      if grid[row,cc] == 0:
        new_row[cc] = color
      elif grid[row,cc] == color:
        break # stop if colors match
      else:
          continue # continue to next if colors don't match

  return new_row