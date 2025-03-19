"""
The transformation involves rearranging the grey (5) pixels from the edges toward the center of the grid, forming a filled rectangle. The red (2) pixels remain in their original locations. The size and shape of the central grey rectangle vary depending on the dimensions of the input grid and the initial arrangement of the grey pixels.
"""

import numpy as np

def find_objects_by_color(grid, color):
    """
    Finds contiguous objects of a specified color in a grid.
    Returns a list of lists, where each inner list contains the (row, col) coordinates of an object's pixels.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and not visited[curr_r, curr_c]:
                        visited[curr_r, curr_c] = True
                        obj.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects.append(obj)
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find grey objects in the input grid
    gray_objects = find_objects_by_color(input_grid, 5)
    
    # Calculate the total number of grey pixels
    total_gray_pixels = sum(len(obj) for obj in gray_objects)

    # Clear existing grey pixels in the output grid
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 5:
                output_grid[r,c] = 0
    
    # Determine the center of the grid
    center_row = rows // 2
    center_col = cols // 2

    # Determine fill dimensions based on grid size and total grey pixels
    # Aim for a roughly square or rectangular fill, centered
    fill_height = 0
    fill_width = 0
    
    if total_gray_pixels > 0 :
      fill_height = int(np.sqrt(total_gray_pixels))
      fill_width = total_gray_pixels // fill_height
    
      # Adjust starting row and col to center the fill
      start_row = center_row - fill_height // 2
      start_col = center_col - fill_width // 2
    
      # Fill the determined area with grey pixels
      for r in range(start_row, start_row + fill_height):
          for c in range(start_col, start_col + fill_width):
              if 0 <= r < rows and 0 <= c < cols: # Boundary check
                output_grid[r, c] = 5

    return output_grid