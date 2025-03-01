"""
The transformation maintains the red shape while modifying the magenta shape. Magenta pixels move inwards one unit towards the nearest edge, but only if the move does not disconnect the magenta shape and does not overlap with any red pixels.
"""

import numpy as np

def get_objects(grid, color):
    """Find connected components of a specific color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        """Depth-first search to find connected pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        object_pixels = [(row, col)]

        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))

        return object_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))

    return objects

def is_connected(pixels):
    """
    Checks if a set of pixels form a connected component using a simple
    adjacency check
    """
    if not pixels:
        return True  # Empty set is considered connected

    # Create a set of pixel coordinates for quick lookup
    pixel_set = set(pixels)

    # Check if the set is connected
    # Starting from the first pixel, do a depth-first search
    visited = set()
    stack = [pixels[0]]

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        # Add unvisited neighbors to the stack
        row, col = current
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        for neighbor in neighbors:
            if neighbor in pixel_set and neighbor not in visited:
                stack.append(neighbor)

    return len(visited) == len(pixel_set)

def transform(input_grid):
    """
    Modify the magenta shape by shifting pixels inwards, avoiding red pixels and maintaining connectivity.
    """
    output_grid = np.copy(input_grid)
    magenta_objects = get_objects(input_grid, 6)
    red_objects = get_objects(input_grid, 2)
    red_pixels = set()
    for obj in red_objects:
      red_pixels.update(obj)
    
    for magenta_object in magenta_objects:
      new_magenta_object = magenta_object.copy()
      for pixel in magenta_object:
        row, col = pixel
        
        # check neighbors
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        
        for neighbor_row, neighbor_col in neighbors:
          # check if move is within grid
          if 0 <= neighbor_row < output_grid.shape[0] and 0 <= neighbor_col < output_grid.shape[1]:

            # Check if neighbor cell is empty (not magenta or red)
            if (neighbor_row,neighbor_col) not in red_pixels and output_grid[neighbor_row,neighbor_col] == 0:
              # check if move breaks connectivity
              temp_object = new_magenta_object.copy()
              temp_object.remove(pixel)
              temp_object.append((neighbor_row, neighbor_col))

              if is_connected(temp_object):
                  # move the pixel
                  output_grid[row,col] = 0
                  output_grid[neighbor_row,neighbor_col] = 6
                  new_magenta_object.remove(pixel)
                  new_magenta_object.append((neighbor_row,neighbor_col))
                  break # move only one step at a time

    return output_grid