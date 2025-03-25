"""
1.  **Identify Objects:** Locate all contiguous regions of red (2) pixels, green (3) pixels, and white/blank (0) pixels.
2.  **Prioritize Green:**  Isolate the green pixels.
3.  **Vertical Shift (Green):** Move all green pixels upwards as far as possible, stopping when they reach the top edge of the grid or encounter another non-white pixel.
4.  **Vertical Shift (red):** shift the red block down, stopping when the top most pixel is one row above the original top most position
5. **Consolidate:** coalesce adjacent same color cells to be connected
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Identify green pixels
    green_pixels = find_objects(input_grid, 3)

    # shift green pixels up
    for green_pixel_group in green_pixels: #each green pixel is in own group
      for r, c in green_pixel_group:
        # Move the green pixel upwards as far as possible.
        new_row = r
        while new_row > 0 and output_grid[new_row - 1, c] == 0:
            new_row -= 1
        output_grid[new_row, c] = 3

    # find red blocks
    red_blocks = find_objects(input_grid, 2)
   
    # shift red blocks
    for red_block in red_blocks:
        #find top most row of this red block
        min_row = min(r for r, _ in red_block)
        
        #shift red block down one from original, if space
        if (min_row + 1) < input_grid.shape[0]: #check within bounds
           target_row = min_row+1
           
           #check for conflicts
           conflict = False
           for r,c in red_block:
              if output_grid[r - min_row + target_row,c] != 0:
                 conflict = True
                 break
           
           if not conflict:
              for r,c in red_block:
                 output_grid[r - min_row + target_row, c] = 2
           else: #cannot shift, put back original block
              for r,c in red_block:
                 output_grid[r,c] = 2

        else: #cannot shift, put back original block
          for r,c in red_block:
            output_grid[r,c] = 2
    

    return output_grid