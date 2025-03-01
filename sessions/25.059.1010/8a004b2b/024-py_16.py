"""
1.  **Identify Single Yellow Pixels:** Locate all single yellow (color 4) pixels within the input grid.
2.  **Move to Corners:** Move these single yellow pixels to the corners of the grid, filling the corners in the following order: top-left, top-right, bottom-left, bottom-right.  If a corner already contains a non-background pixel, skip that corner and proceed to the next available corner in the sequence. If there are more single yellow pixels than available corners, place only as many as will fit in available corners and do not move the remainder.
3. **Fill to Right-most Non-Zero:** For any given row, fill all 0's to the left of the right-most non-zero color with that color.

"""

import numpy as np

def find_single_pixels(grid, color):
    """Finds single pixels of the specified color."""
    single_pixels = []
    rows, cols = grid.shape
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def is_single(r, c, color):
      if not is_valid(r,c) or grid[r,c] != color:
        return False

      neighbors = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
      for nr, nc in neighbors:
        if is_valid(nr, nc) and grid[nr, nc] == color:
          return False

      return True

    for r in range(rows):
      for c in range(cols):
        if is_single(r,c, color):
          single_pixels.append((r,c))

    return single_pixels

def fill_rows_to_rightmost(grid):
    """Fills each row with the right-most non-zero color."""
    output_grid = np.copy(grid)
    rows, cols = output_grid.shape
    for r in range(rows):
        rightmost_color = 0
        for c in range(cols - 1, -1, -1):
            if output_grid[r, c] != 0:
                rightmost_color = output_grid[r, c]
            elif rightmost_color != 0:
                output_grid[r, c] = rightmost_color
    return output_grid

def move_pixels_to_corners(grid, pixels, color):
    """
    Moves specified pixels to the corners, filling them in order:
    top-left, top-right, bottom-left, bottom-right.
    Skips occupied corners.
    """
    output_grid = np.copy(grid)
    rows, cols = output_grid.shape
    corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]
    pixel_idx = 0

    for cr, cc in corners:
        if pixel_idx < len(pixels):
           if output_grid[cr,cc] == 0:
                #Remove the pixel at old location, set to background
                output_grid[pixels[pixel_idx][0], pixels[pixel_idx][1]] = 0
                #Set new corner location to color
                output_grid[cr, cc] = color
                pixel_idx +=1
        else:
            break #no more pixels to move

    return output_grid

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Find single yellow pixels
    yellow_pixels = find_single_pixels(output_grid, 4)

    # 2. Move yellow pixels to corners
    output_grid = move_pixels_to_corners(output_grid, yellow_pixels, 4)
    
    # 3. Fill to rightmost
    output_grid = fill_rows_to_rightmost(output_grid)

    return output_grid