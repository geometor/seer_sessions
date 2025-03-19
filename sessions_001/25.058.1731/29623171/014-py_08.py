"""
1.  **Identify Gray Structures:** Find all horizontal gray lines (contiguous sequences of gray pixels) and all vertical gray columns in the input grid.
2.  **Categorize Red Pixels:** For each red pixel, determine its position relative to the gray lines:
    *   **Above:** If the red pixel's row is above *any* gray line.
    *   **Below:** If the red pixel's row is below *any* gray line.
    * **On:** If the Red Pixel's row is *on* any gray line.
3.  **Transform Red Pixels:**
    *   **Above any Gray Line:** If a red pixel is above any gray line AND left of a gray column AND is adjacent to a White(0) pixel horizontally, extend it to the right, changing White(0) pixels to Red(2), until it encounters a gray column, the edge of the grid, or another Red(2) pixel.
    *   **Below any Gray Line:** Change the red pixel to white (0).
    *   **On any Gray Line:** The red pixel should remain unchanged.
4.  **Output:** Create the output grid with these transformations, keeping all other pixels (gray and white) unchanged from the input.
"""

import numpy as np

def find_pixels(grid, color):
    # Find coordinates of pixels with the specified color.
    return np.array(np.where(grid == color)).T

def find_gray_lines(grid):
    # Find all horizontal gray lines.
    gray_pixels = find_pixels(grid, 5)
    gray_lines = {}
    for r, c in gray_pixels:
        if r not in gray_lines:
            gray_lines[r] = []
        gray_lines[r].append(c)
    return gray_lines

def find_gray_columns(grid):
    # Find all vertical gray columns
    gray_pixels = find_pixels(grid, 5)
    gray_columns = {}
    for r, c in gray_pixels:
        if c not in gray_columns:
            gray_columns[c] = []
        gray_columns[c].append(r)
    return gray_columns
    
def is_above_any_gray_line(row, gray_lines):
    # Check if a given row is above any gray line.
  for gray_row in gray_lines:
    if row < gray_row:
      return True
  return False

def is_below_any_gray_line(row, gray_lines):
    # Check if a given row is below any gray line.
  for gray_row in gray_lines:
    if row > gray_row:
      return True
  return False

def is_on_any_gray_line(row, gray_lines):
  return row in gray_lines

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # find red pixels
    red_pixels = find_pixels(input_grid, 2)

    # find gray lines and columns
    gray_lines = find_gray_lines(input_grid)
    gray_columns = find_gray_columns(input_grid)
    sorted_gray_columns = sorted(gray_columns.keys())
    
    # iterate over red pixels
    for r, c in red_pixels:
        # categorize and transform red pixels
        if is_above_any_gray_line(r, gray_lines):
          for col_index in sorted_gray_columns:
            if c < col_index:
                # Check if the next pixel to right is White
                if c + 1 < cols and output_grid[r,c+1] == 0:
                    # Extend red to the right until obstacle
                    for i in range(c + 1, col_index):
                        if i < cols and output_grid[r, i] == 0:
                            output_grid[r, i] = 2
                        else:
                            break  # Stop at any obstacle (non-white pixel)
                break  # Stop searching columns, proceed to next red

        elif is_below_any_gray_line(r, gray_lines):
          output_grid[r, c] = 0
        elif is_on_any_gray_line(r,gray_lines):
          continue #do nothing, pixel remains
    return output_grid.tolist()