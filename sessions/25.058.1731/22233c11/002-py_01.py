"""
1.  **Identify Green Objects:** Locate all green (3) pixels in the input grid.
2.  **Bounding Box:** For each contiguous group of green pixels, construct an axis-aligned bounding box.
3.  **Place Azure Pixels:** For a single green pixel at row `r` and column `c`, and azure pixel is placed at `r-1`, `c-1`
4.  **Output:** Create the output grid with the original green pixels and the newly placed azure pixels.
"""

import numpy as np

def get_green_pixels(grid):
    """Finds coordinates of all green pixels in the grid."""
    green_pixels = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 3:
                green_pixels.append((r, c))
    return green_pixels

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    green_pixels = get_green_pixels(input_grid)

   # Calculate the bounding box corners for a 2x2 green object,
   # assuming only one such object may exist at a time.
    
    min_r, min_c = 100, 100
    max_r, max_c = -1, -1

    for r,c in green_pixels:
      min_r = min(min_r, r)
      min_c = min(min_c, c)
      max_r = max(max_r, r)
      max_c = max(max_c, c)
        

    if (max_r - min_r == 1) and (max_c - min_c ==1):
        if min_r > 0 and min_c > 0:
              output_grid[min_r - 1, min_c -1 ] = 8
        if max_r+1 < output_grid.shape[0] and max_c+1 < output_grid.shape[1]:
            output_grid[max_r+1, max_c + 1] = 8

        if min_r > 0 and max_c + 1 < output_grid.shape[1]:
          output_grid[min_r - 1, max_c + 1] = 8
        
        if min_c > 0 and max_r + 1 < output_grid.shape[0]:
          output_grid[max_r +1, min_c -1] = 8
    else:
      for r, c in green_pixels:
          if r > 0 and c > 0:
              output_grid[r - 1, c - 1] = 8
          if r + 1 < output_grid.shape[0] and c + 1 < output_grid.shape[1]:
              output_grid[r + 1, c + 1] = 8
    return output_grid.tolist()