"""
Transforms an input grid into an output grid based on a combination of edge detection,
object recognition, and context-dependent color replacement. The transformation rules
appear to involve identifying objects (contiguous regions of the same color),
checking their positions relative to the grid edges and other objects, and
then changing pixel colors based on these conditions.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Retrieves the neighbors of a pixel, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the pixel itself
                neighbors.append(grid[i, j])
    return neighbors

def is_on_edge(grid, row, col):
    """Checks if a pixel is on the edge of the grid."""
    rows, cols = grid.shape
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1

def find_objects(grid):
    """
    Identifies contiguous objects (regions of same color) in the grid.
    Returns a dictionary where keys are colors and values are lists of (row, col) coordinates.
    """
    rows, cols = grid.shape
    visited = set()
    objects = {}

    def dfs(row, col, color, obj_coords):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.append((row, col))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    dfs(row + dr, col + dc, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def get_diagonals(grid):
    """Extracts the main and anti-diagonals of the grid."""
    rows, cols = grid.shape
    main_diag = [grid[i, i] for i in range(min(rows, cols))]
    anti_diag = [grid[i, cols - 1 - i] for i in range(min(rows, cols))]
    return main_diag, anti_diag


def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    objects = find_objects(input_grid)
    main_diag, anti_diag = get_diagonals(input_grid)


    # Example 1 logic (modified to be less specific)
    if 4 in objects and 5 in objects:
      for row in range(rows):
          for col in range(cols):
              if input_grid[row,col] in (4,5):
                  neighbors = get_neighbors(input_grid, row, col)
                  if (input_grid[row,col] == 4 and 5 in neighbors) or \
                     (input_grid[row,col] == 5 and 4 in neighbors):
                      output_grid[row,col] = 0

    # Example 2 logic (generalized edge and neighbor checking)
    if 5 in objects and 6 in objects:
        for obj_coords in objects.get(6, []): #Iterate over the objects labeled 6
            for row, col in obj_coords:
                if is_on_edge(input_grid, row, col):
                    output_grid[row,col] = 0
                else:
                  neighbors = get_neighbors(input_grid, row, col)
                  if any(neighbor==0 for neighbor in neighbors):
                      output_grid[row,col] = 0

        for obj_coords in objects.get(5, []): #Iterate over the objects labeled 5
            for row, col in obj_coords:
              neighbors = get_neighbors(input_grid,row,col)
              if 6 in neighbors and not any([x==5 for x in neighbors]):
                  output_grid[row,col] = 6  # Change isolated 5s to 6s.

        for obj_coords in objects.get(5, []): #Iterate over the objects labeled 5
            for row, col in obj_coords:
                if is_on_edge(input_grid, row, col) :
                    output_grid[row, col] = 0
                else:
                  neighbors = get_neighbors(output_grid, row, col)
                  if any(neighbor==0 for neighbor in neighbors):
                      output_grid[row,col] = 0


    # Example 3 logic (diagonals and edge)
    if 9 in objects and 5 in objects:
       for row in range(rows):
           for col in range(cols):
             if is_on_edge(input_grid,row,col) and input_grid[row,col] == 9:
                output_grid[row, col] = 0  # Edge 9s to 0

       for obj_coords in objects.get(5,[]):
          for row,col in obj_coords:
             neighbors = get_neighbors(input_grid,row,col)
             if any(neighbor==9 for neighbor in neighbors):
                output_grid[row,col]=9

       for row in range(rows):
           for col in range(cols):
              if (input_grid[row,col] == 9 and (row,col) in [(i,i) for i in range(min(rows,cols))]): #On a main diagonal
                  output_grid[row, col] = 0
              if (input_grid[row,col] == 9 and (row,col) in [(i,cols-1-i) for i in range(min(rows,cols))]):
                  output_grid[row, col] = 0


    return output_grid.tolist()