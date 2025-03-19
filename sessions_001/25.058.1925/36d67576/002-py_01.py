"""
This program transforms an input grid of colored pixels into an output grid based on the following rules:

1.  **Identify Objects:** Find contiguous blocks of non-zero pixels. Consider these as distinct objects.
2.  **Observe Changes:** Compare the input and output grids. Note which objects have changed in color, position, or slightly changed in shape.
3.  **Prioritize Actions**:
    *   If there is a single Blue(1) pixel within an orange(4) object, change that orange pixel at the location to Blue(1)
    *   If there is a Green(3) object adjacent to an Orange(4) or Blue(1) objects, change the color of adjacent pixels to match the Orange(4) or Blue(1)
    *   The single Red(2) pixel does not appear to move
4.  **Apply Changes:** Iterate through the grid, applying the color and shape changes based on the rules identified above, prioritizing rules in that order.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append((grid[row,col], obj)) #store color with the object
    return objects

def get_neighbors(grid, row, col):
  """get the neighbors of a given cell"""
  neighbors = []
  for i in range(-1,2):
      for j in range(-1,2):
        if (i==0 and j==0):
            continue
        n_row = row + i
        n_col = col + j
        if (0 <= n_row < grid.shape[0] and 0 <= n_col < grid.shape[1]):
          neighbors.append((n_row, n_col))
  return neighbors
    

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = input_grid.copy()
    objects = find_objects(input_grid)

    # Apply rule: Blue(1) pixel within Orange(4) object takes precedence
    for color, obj in objects:
        if color == 1: # Blue
            for r, c in obj:
                neighbors = get_neighbors(input_grid, r,c)
                for nr, nc in neighbors:
                    if input_grid[nr,nc] == 4:
                        output_grid[nr, nc] = 1


    # Apply Rule: Green(3) near Orange(4)/Blue(1) modifies those
    for color, obj in objects:
        if color == 3:
            for r, c in obj:
              neighbors = get_neighbors(input_grid, r,c)
              for nr, nc in neighbors:
                  if input_grid[nr,nc] == 4 or input_grid[nr,nc] ==1 :
                      output_grid[r,c]= input_grid[nr,nc]
    
    # Apply Rule: Blue near an object changes the color
    for color, obj in objects:
        if color == 1:
            for r, c in obj:
                neighbors = get_neighbors(input_grid, r, c)
                for nr, nc in neighbors:
                    if (input_grid[nr,nc] != 0 and output_grid[nr,nc]!= 1) : # If neighbor not blank
                        output_grid[nr,nc] = input_grid[nr, nc]


    return output_grid