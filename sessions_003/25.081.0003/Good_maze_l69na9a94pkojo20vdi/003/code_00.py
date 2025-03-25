"""
1.  **Identify the Maze:** Find all yellow (4) pixels in the input grid. These pixels form a connected "maze" or path. We'll assume 4-connectivity for the maze.
2.  **Identify Inside Pixels:** Identify the red (2) pixels that lie inside the maze defined by the yellow path. This will use a flood-fill approach, starting outside the maze.
3.  **Replace Inside Red Pixels:** Change the color of all identified "inside" red pixels to azure (8).
4.  **Preserve Background:** Leave all black (0) pixels unchanged.
"""

import numpy as np
from collections import deque

def get_neighbors(grid, pos, connectivity=4):
    """Returns the valid neighbors of a position in the grid."""
    r, c = pos
    neighbors = []
    height, width = grid.shape

    if connectivity == 4:
        possible_neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    elif connectivity == 8:
        possible_neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1),
                              (r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]
    else:
        raise ValueError("Connectivity must be 4 or 8.")

    for nr, nc in possible_neighbors:
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def find_maze_pixels(grid):
    """Finds all pixels that are part of the yellow (4) maze."""
    return np.array(np.where(grid == 4)).T

def is_inside_maze(grid, start_pos):
   """
   Determines if a given starting position is inside the maze
   """
   # create a copy, so we can modify without changing original
   grid_copy = np.copy(grid)
   height, width = grid_copy.shape

   # Mark the starting position
   if grid_copy[start_pos] == 4:
       return False

   # do the fill.
   queue = deque([start_pos])
   visited = set()

   while queue:
     curr_pos = queue.popleft()

     if curr_pos in visited:
      continue
     visited.add(curr_pos)

     neighbors = get_neighbors(grid_copy, curr_pos, connectivity = 4)

     for neighbor in neighbors:
        if grid_copy[neighbor] != 4:
           queue.append(neighbor)

   # check if any edge was reached
   for r, c in visited:
     if r == 0 or r == height - 1 or c == 0 or c == width - 1:
        return False

   return True

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid).astype(int)
    height, width = output_grid.shape

    # Identify maze pixels
    maze_pixels = find_maze_pixels(input_grid)

    # Iterate through all red pixel locations
    for r in range(height):
      for c in range(width):
        if output_grid[r,c] == 2: # Check if it's red
          # Determine if red is inside
          if is_inside_maze(input_grid, (r,c)):
            # If so, change to azure (8)
            output_grid[r,c] = 8
            

    return output_grid