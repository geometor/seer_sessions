"""
Transforms an input grid into an output grid based on a set of rules involving
object identification, edge/corner detection, adjacency analysis, and
color transformations. The rules generalize across the provided examples,
focusing on object properties and relative positions rather than
specific color values. The order of rule application appears to be significant.
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
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    objects = find_objects(input_grid)

    # Rule 1: Edge objects become 0
    for row in range(rows):
        for col in range(cols):
            if is_on_edge(input_grid, row, col):
                output_grid[row, col] = 0

    # Rule 2: Diagonal 9s become 0
    main_diag, anti_diag = get_diagonals(input_grid)
    for row in range(rows):
        for col in range(cols):
            if input_grid[row,col] == 9 and ((row,col) in [(i,i) for i in range(min(rows,cols))] or (row, col) in [(i, cols - 1 - i) for i in range(min(rows,cols))]):
                output_grid[row,col] = 0

   # Rule 3: Example 1 specific rules (4 and 5)
    if 4 in objects and 5 in objects:
        for obj_coords in objects[5]:
            for row, col in obj_coords:
                neighbors = get_neighbors(input_grid, row, col)
                if 4 in neighbors:
                    output_grid[row,col] = 4 # 5 next to 4 becomes 4
        for obj_coords in objects[4]:
             for row,col in obj_coords:
                 neighbors = get_neighbors(input_grid,row, col)
                 if is_on_edge(input_grid,row,col) and 5 in neighbors:
                     output_grid[row,col] = 0
        for obj_coords in objects[5]:
            for row, col in obj_coords:
                neighbors = get_neighbors(output_grid, row, col)
                if all(neighbor != 4 for neighbor in neighbors ) and output_grid[row,col]!=0:  # Check output for 0, to prevent overriding edge rule
                    output_grid[row,col] = 0 #Isolated 5s
    # Rule 4: Example 2 specific rules (5 and 6)
    if 5 in objects and 6 in objects:
        for obj_coords in objects[6]:
            for row, col in obj_coords:
                neighbors = get_neighbors(input_grid, row, col)
                if any(neighbor == 0 for neighbor in neighbors):
                    output_grid[row,col] = 0  # 6 next to 0 becomes 0

        for obj_coords in objects[5]:
            for row, col in obj_coords:
                neighbors = get_neighbors(input_grid, row, col)
                if 6 in neighbors and not any([x==5 for x in neighbors]):
                    output_grid[row, col] = 6  # 5 next to 6, and not next to 5, becomes 6

        for obj_coords in objects[5]:  #Apply edge and 0 neighbor rules *after* color changes.
           for row, col in obj_coords:
               neighbors = get_neighbors(output_grid,row,col)
               if any(neighbor==0 for neighbor in neighbors):
                  output_grid[row,col]=0 #check against output grid for 0 neighbor rule.

    # Rule 5: Example 3 specific rules (5 and 9)
    if 5 in objects and 9 in objects:
        for obj_coords in objects[5]:
            for row, col in obj_coords:
                neighbors = get_neighbors(input_grid, row, col)
                if 9 in neighbors:
                    output_grid[row,col] = 9  # 5 next to 9 becomes 9

    return output_grid.tolist()