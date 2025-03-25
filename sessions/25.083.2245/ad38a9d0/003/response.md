```python
"""
Transforms magenta (6) and orange (7) pixels in the input grid based on their
neighborhood and contiguity, while leaving other colored pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)
    magenta_pixels = find_pixels(input_grid, 6)
    orange_pixels = find_pixels(input_grid, 7)

    # Transform magenta pixels.
    for i, j in magenta_pixels:
        output_grid[i, j] = transform_magenta(input_grid, i, j)

    # Transform orange pixels.
    for i, j in orange_pixels:
        output_grid[i,j] = transform_orange(input_grid, i, j)

    return output_grid

def find_pixels(grid, color):
    """
    Finds the coordinates of all pixels of a given color.
    """
    return list(zip(*np.where(grid == color)))

def transform_magenta(input_grid, i, j):
    """Determine transformation for magenta based on observations"""
    # get the object that includes (i,j)
    magenta_object = get_object(input_grid, i, j, 6)

    # find the vertical/horizontal bounds
    min_row = min([p[0] for p in magenta_object])
    max_row = max([p[0] for p in magenta_object])
    min_col = min([p[1] for p in magenta_object])
    max_col = max([p[1] for p in magenta_object])

    if (max_row - min_row) <= 1 and (max_col - min_col) <= 2: # small horizontal
      if i == min_row: return 8 if j > (input_grid.shape[1] // 2) else 4
      else: return 8 if j > (input_grid.shape[1] // 2) else 4

    if i == max_row: return 5 # bottom of grid
    
    # transform differently by row
    # this could be generalized to position within the object, but more data is
    # required
    if i == min_row : return 8 if j > (input_grid.shape[1]//2) else 4 #top row
    if i == min_row+1 : return 9 if j > (input_grid.shape[1]//2) else 3 #top row+1
    if i == min_row +2: return 9 if j > (input_grid.shape[1]//2) else 3
    if i == min_row + 3: return 4 if j > (input_grid.shape[1]//2) else 2

    
    return 6

def transform_orange(input_grid, i, j):
    """Determine transformation for orange based on observations"""
      
    neighbors = get_neighbors(input_grid, i, j)
    for x, y in neighbors:
        if input_grid[x, y] == 6:
            return 4
    return 7


def get_neighbors(grid, i, j):
    """
    Gets the coordinates of the neighbors of a pixel (including diagonals).
    """
    rows, cols = grid.shape
    neighbors = []
    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if (x, y) != (i, j):
                neighbors.append((x, y))
    return neighbors

def get_object(grid, row, col, color):
  """
  Finds a contiguous object in the grid starting at the given row and column.
  """
  rows, cols = grid.shape
  visited = set()
  to_visit = [(row, col)]
  object_pixels = []

  while to_visit:
      current_row, current_col = to_visit.pop()

      if (current_row, current_col) in visited:
          continue
      visited.add((current_row, current_col))

      if 0 <= current_row < rows and 0 <= current_col < cols and grid[current_row, current_col] == color:
        object_pixels.append((current_row, current_col))
        # Add neighbors to the list of cells to visit
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                to_visit.append((current_row + dr, current_col + dc))

  return object_pixels

```