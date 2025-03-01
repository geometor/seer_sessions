"""
The transformation recolors objects below the top row of the input grid based on the colors of single-pixel objects in the top row. Objects in rows other than the top row are recolored to match the color of the single-pixel object in the same column on the top row. The background (color 0) and the single-color objects in the top row remain unchanged.
"""

import numpy as np

def get_top_row_colors(grid):
    """
    Gets the colors and their column indices from the top row of the grid.
    Returns a dictionary where keys are column indices and values are colors.
    """
    top_row_colors = {}
    for col_index, color in enumerate(grid[0]):
        if color != 0:  # Exclude background color
            top_row_colors[col_index] = color
    return top_row_colors

def find_objects(grid):
    """
    Finds contiguous objects (regions of same color) in the grid, excluding the background color (0).
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append(current_object)
    return objects
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the colors and their column positions from the top row
    top_row_colors = get_top_row_colors(input_grid)

    # Find all objects in the grid
    all_objects = find_objects(input_grid)
    
    # Iterate through all objects except in the first row
    for obj in all_objects:
      is_top_row = False
      for r,c in obj:
        if r == 0:
          is_top_row = True
          break
      if not is_top_row:
        #if the object is below the top row
        for row, col in obj:
          #find color for the object
          if col in top_row_colors:
            #recolor pixels based on color map
            output_grid[row, col] = top_row_colors[col]

    return output_grid