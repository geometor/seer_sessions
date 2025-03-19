"""
1.  **Identify Key Pixels:** Locate all red (2) and yellow (4) pixels in the input grid.
2.  **Expansion:** For each red and yellow pixel:
    *   If a red pixel is on a row with another colored pixel, expand it vertically to create a 3x1 shape
    *   If a red pixel is on a column with another colored pixel, expand it horizontally to create a 1x3 shape
    *   If a red pixel is on a row and a column with another colored pixel, expand it to a 3x3 square
    *   Apply the same logic to yellow pixels.
3.  **Intersection:** Where the expanded regions of red and yellow pixels overlap, place a gray (5) pixel.
4.  **Background:** All remaining white (0) pixels in the input become white (0) pixels in the output.
5. **Preserve Layout:** Maintain the relative spatial positions of the expanded red and yellow pixels according to the input grid.
"""

import numpy as np

def get_colored_pixels(grid, color):
    """Finds coordinates of pixels of a specific color."""
    return np.argwhere(grid == color)

def expand_pixel(grid, coord, color):
    """Expands a pixel based on its neighbors."""
    row, col = coord
    height, width = grid.shape
    output_grid = np.copy(grid)

    # Check for other colored pixels in the same row and column
    has_colored_neighbor_row = any(grid[row, c] in [2, 4] and c != col for c in range(width))
    has_colored_neighbor_col = any(grid[r, col] in [2, 4] and r != row for r in range(height))

    if has_colored_neighbor_row and has_colored_neighbor_col:
      # Expand to 3x3
      for i in range(max(0, row - 1), min(height, row + 2)):
          for j in range(max(0, col - 1), min(width, col + 2)):
              output_grid[i, j] = color
    elif has_colored_neighbor_row:
      # Expand vertically (3x1)
      for i in range(max(0, row - 1), min(height, row + 2)):
          output_grid[i, col] = color
    elif has_colored_neighbor_col:
       # Expand horizontally (1x3)
      for j in range(max(0, col - 1), min(width, col + 2)):
        output_grid[row, j] = color
    else:
        output_grid[row,col] = color # no change

    return output_grid

def handle_intersections(grid):
    """Places gray pixels at intersections of expanded red and yellow regions."""
    output_grid = np.copy(grid)
    red_pixels = get_colored_pixels(grid, 2)
    yellow_pixels = get_colored_pixels(grid, 4)

    for r_row, r_col in red_pixels:
        for y_row, y_col in yellow_pixels:
            if (r_row == y_row and abs(r_col - y_col) <= 2 ) or \
               (r_col == y_col and abs(r_row-y_row)<=2)  or \
               (abs(r_row - y_row) <=2 and abs(r_col - y_col) <=2):
                #find the intersection
                if grid[r_row,r_col] != 0 and grid[y_row, y_col] !=0:
                    #check if the shapes intersect
                    min_row = max(min(r_row,y_row)-1,0)
                    max_row = min(max(r_row,y_row)+2,grid.shape[0])
                    min_col = max(min(r_col, y_col)-1, 0)
                    max_col = min(max(r_col, y_col)+2,grid.shape[1])

                    for i in range(min_row, max_row):
                        for j in range(min_col, max_col):
                            if grid[i,j] in [2,4]:
                                output_grid[i,j] = 5

    return output_grid

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    output_grid = np.zeros_like(input_grid)

    red_pixels = get_colored_pixels(input_grid, 2)
    yellow_pixels = get_colored_pixels(input_grid, 4)

    # Expand red pixels
    for coord in red_pixels:
        output_grid = expand_pixel(output_grid, coord, 2)

    # Expand yellow pixels
    for coord in yellow_pixels:
      output_grid = expand_pixel(output_grid, coord, 4)


    output_grid = handle_intersections(output_grid)

    return output_grid