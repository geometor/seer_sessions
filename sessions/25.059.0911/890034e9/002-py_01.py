"""
The transformation rule involves identifying a "marker" shape (azure/light blue in Examples 1 and 2, a frame of yellow/red in Example 3) and a "target" shape (red in example 1, light blue in example 2, yellow in example 3). The target shape's pixels fill the output in the location of the marker shape, by replacing what is there.
"""

import numpy as np

def find_shape(grid, color):
    """Finds contiguous blocks of a specific color in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    shapes = []

    def dfs(row, col):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        shape = [(row, col)]

        shape.extend(dfs(row + 1, col))
        shape.extend(dfs(row - 1, col))
        shape.extend(dfs(row, col + 1))
        shape.extend(dfs(row, col - 1))
        return shape
    
    for i in range(rows):
        for j in range(cols):
            if grid[i,j] == color and not visited[i,j]:
                shapes.append(dfs(i,j))

    return shapes

def get_marker_and_target(grid):
    """
    Identifies marker shape, based on specific criteria.
    """
    
    
    azure_shapes = find_shape(grid, 8)
    if (len(azure_shapes) > 0):
        marker_shape = azure_shapes[0] #take first azure shape
        red_shapes = find_shape(grid, 2)
        #find the largest shape, that is not the azure one, but the red.
        if(len(red_shapes) > 0):
          target_shape = red_shapes[0]
          
          #now make them real shapes
          marker_shape = np.array(marker_shape)
          target_shape = np.array(target_shape)

          return marker_shape, target_shape, 2, 8

    light_blue_shapes = find_shape(grid, 8)
    
    if (len(light_blue_shapes) > 0):
      
      #find the biggest light blue shape
      max_len = 0
      for i in range(len(light_blue_shapes)):
          if(len(light_blue_shapes[i]) > max_len):
              marker_shape = light_blue_shapes[i]
              max_len = len(light_blue_shapes[i])

      target_shape = marker_shape #light_blue is the target too
      marker_shape = np.array(marker_shape)
      target_shape = np.array(target_shape)

      return marker_shape, target_shape, 8, 8
    

    yellow_shapes = find_shape(grid, 4)
    if(len(yellow_shapes) > 0):
      target_shape = yellow_shapes[0]
      target_shape = np.array(target_shape)
      #marker is the rectangle
      min_r, min_c = np.min(target_shape, axis=0)
      max_r, max_c = np.max(target_shape, axis=0)
      marker_shape = []

      # Add top and bottom borders
      for c in range(min_c - 1, max_c + 2):
          marker_shape.append((min_r - 1, c))
          marker_shape.append((max_r + 1, c))

      # Add left and right borders, avoiding corners
      for r in range(min_r, max_r + 1):
          marker_shape.append((r, min_c - 1))
          marker_shape.append((r, max_c + 1))
      
      marker_shape = np.array(marker_shape)
      #replace 2s with 4s
      for i in range(len(marker_shape)):
        r, c = marker_shape[i]
        if(grid[r,c] == 2):
          grid[r,c] = 4

      return marker_shape, target_shape, 4, 4
    
    return [], [], 0, 0


def transform(input_grid):
    """
    Transforms the input grid based on identified shapes and their colors,
    replacing some parts.
    """
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(grid)

    # Find and identify the marker and target shapes
    marker_shape, target_shape, target_color, marker_color = get_marker_and_target(grid)
    if (len(marker_shape) == 0): #no marker, return
      return output_grid

    #find the bounding box for the marker_shape
    marker_min_row = np.min(marker_shape[:, 0])
    marker_min_col = np.min(marker_shape[:, 1])

    # Iterate through target shape and fill them in
    if (len(target_shape) > 0):
      for r, c in target_shape:
          output_grid[r, c] = target_color

    return output_grid.tolist()