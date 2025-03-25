"""
Transforms an input grid by identifying objects and applying absorption and extension transformations based on their adjacency and color.
Objects adjacent to different colored objects on the right are absorbed by the object on the right. Color 2 has unique behavior of absorbing adjacent colors 1 and 5 on its left. Color 3 extends based on adjacent cells.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    """Determines the most frequent (background) color in the grid."""
    flattened = grid.flatten()
    count = Counter(flattened)
    return count.most_common(1)[0][0]

def find_objects(grid, background_color):
    """Identifies connected components (objects) of non-background colors."""
    visited = set()
    objects = []

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] == background_color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)
        dfs(row + 1, col + 1, current_object)
        dfs(row - 1, col - 1, current_object)
        dfs(row + 1, col - 1, current_object)
        dfs(row - 1, col + 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != background_color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append((grid[row,col], current_object))  # Store color and object
    return objects

def get_neighbors(grid, pixel):
    """Get the neighbors, including diagonals"""
    row,col = pixel
    neighbors = []
    for i in range(-1,2):
        for j in range(-1,2):
            if i==0 and j == 0:
                continue
            neighbor_row, neighbor_col = row+i, col+j
            if 0 <= neighbor_row < grid.shape[0] and 0 <= neighbor_col < grid.shape[1]:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors
    
def transform(input_grid):
    """Applies the transformation rules to the input grid."""
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    background_color = get_background_color(grid)
    objects = find_objects(grid, background_color)

    # Create a dictionary to store objects by color
    objects_by_color = {}
    for color, obj in objects:
        if color not in objects_by_color:
            objects_by_color[color] = []
        objects_by_color[color].append(obj)


    # Absorption and Color 2 specific absorption
    for color, object_pixels_list in objects_by_color.items():
      for object_pixels in object_pixels_list:
        for row, col in object_pixels:
            neighbors = get_neighbors(grid, (row, col))

            # Right-side absorption.
            for n_row, n_col in neighbors:
              if n_col > col and grid[n_row, n_col] != color and grid[n_row, n_col] != background_color:
                absorbing_color = grid[n_row, n_col]
                for r, c in object_pixels:
                  output_grid[r, c] = absorbing_color

            # color 2 absorbs 1 and 5 to the left.
            if color == 2:
                for n_row, n_col in neighbors:
                    if n_col < col and grid[n_row,n_col] in [1,5]:
                        for r,c in object_pixels:
                            output_grid[r,c] = 2

    # Handle object 3 extension.
    if 3 in objects_by_color:
      object3_pixels = []
      for obj_list in objects_by_color[3]:
          object3_pixels.extend(obj_list)

      for r,c in object3_pixels:
          neighbors = get_neighbors(grid,(r,c))
          for n_r, n_c in neighbors:
            if grid[n_r, n_c] != background_color and grid[n_r, n_c] != 3:
                if n_c < c: # extend right
                    for i in range(c+1, grid.shape[1]):
                        output_grid[r,i] = 3
                if n_c > c: # extend left
                    for i in range(0, c):
                        output_grid[r,i] = 3
                if n_r < r: # extend down
                    for i in range(r+1, grid.shape[0]):
                        output_grid[i,c] = 3
                if n_r > r: # extend up
                    for i in range(0,r):
                        output_grid[i,c] = 3

    return output_grid.tolist()