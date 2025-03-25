```python
"""
The transformation rule involves moving non-azure pixels (not 8) that are 1) adjacent to azure pixels (8) and 2) on a specified edge of the grid. These pixels are 'shifted' one position towards the interior of the grid, in the direction of their adjacent azure pixel. Each example focuses on a single edge (left, top, right, or bottom).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid neighbors (coordinates) for a given cell in the grid.
    Considers only horizontal and vertical neighbors, not diagonal.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Determine which edge to process (based on examples, assume only one edge per task)
    # For generalization, we can check all edges, but examples suggest one dominant edge.
    # Let's try left first based on train_1, then adapt if necessary.
    
    
    edges_to_check = []

    # Check left edge
    left_edge_diff = 0
    for r in range(rows):
      if input_grid[r,0] != 8:
          neighbors = get_neighbors(input_grid, r, 0)
          for nr, nc in neighbors:
            if input_grid[nr,nc] == 8:
              left_edge_diff+=1
              break
    if left_edge_diff>0:
      edges_to_check.append("left")

    # Check top edge
    top_edge_diff = 0
    for c in range(cols):
      if input_grid[0,c] != 8:
          neighbors = get_neighbors(input_grid, 0, c)
          for nr, nc in neighbors:
              if input_grid[nr,nc] == 8:
                top_edge_diff+=1
                break
    if top_edge_diff>0:
      edges_to_check.append("top")

    #check right edge
    right_edge_diff = 0
    for r in range(rows):
      if input_grid[r,cols-1] != 8:
          neighbors = get_neighbors(input_grid, r, cols-1)
          for nr, nc in neighbors:
            if input_grid[nr,nc] == 8:
              right_edge_diff+=1
              break
    if right_edge_diff > 0:
      edges_to_check.append("right")

    # Check bottom edge
    bottom_edge_diff = 0
    for c in range(cols):
      if input_grid[rows-1,c] != 8:
          neighbors = get_neighbors(input_grid, rows-1, c)
          for nr, nc in neighbors:
            if input_grid[nr,nc] == 8:
              bottom_edge_diff+=1
              break
    if bottom_edge_diff > 0:
      edges_to_check.append("bottom")

    for edge in edges_to_check:

      if edge == "left":
          for r in range(rows):
              if input_grid[r, 0] != 8:  # Non-azure pixel on the left edge
                  neighbors = get_neighbors(input_grid, r, 0)
                  for nr, nc in neighbors:
                      if input_grid[nr, nc] == 8:  # Adjacent to azure
                          output_grid[r, 0] = 8 # set to azure
                          output_grid[nr,nc] = input_grid[r,0] # move
                          break  # only shift once
      elif edge == "top":
          for c in range(cols):
              if input_grid[0, c] != 8:  # Non-azure pixel on the top edge
                  neighbors = get_neighbors(input_grid, 0, c)
                  for nr, nc in neighbors:
                      if input_grid[nr, nc] == 8:  # Adjacent to azure
                          output_grid[0,c] = 8
                          output_grid[nr, nc] = input_grid[0,c] # move
                          break  # only shift once

      elif edge == "right":
        for r in range(rows):
            if input_grid[r, cols-1] != 8:  # Non-azure pixel on the right edge
                neighbors = get_neighbors(input_grid, r, cols-1)
                for nr, nc in neighbors:
                    if input_grid[nr, nc] == 8:  # Adjacent to azure
                        output_grid[r, cols-1] = 8 # set to azure
                        output_grid[nr,nc] = input_grid[r,cols-1] # move
                        break  # only shift once

      elif edge == "bottom":
        for c in range(cols):
          if input_grid[rows-1,c] != 8:
            neighbors = get_neighbors(input_grid,rows-1,c)
            for nr, nc in neighbors:
              if input_grid[nr,nc] == 8:
                output_grid[rows-1,c] = 8
                output_grid[nr,nc] = input_grid[rows-1,c]
                break

    return output_grid
```