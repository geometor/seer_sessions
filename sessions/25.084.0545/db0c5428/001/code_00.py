"""
Transforms an input grid by identifying objects, mirroring/inverting parts of them,
and applying color changes within the mirrored regions. The azure background is
mostly preserved. The transformation seems to involve a complex mirroring or
inversion of subregions within each object, coupled with specific color
substitutions within those mirrored areas.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of objects within the grid.
    Each object is a set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object, color):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.add((row, col))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            dfs(row + dr, col + dc, current_object, color)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 8 and (row, col) not in visited:
                current_object = set()
                dfs(row, col, current_object, grid[row, col])
                objects.append((grid[row, col], current_object))  # Store color with object
    return objects

def apply_color_mapping(mirrored_region, input_grid, output_grid):
   
    """
    Applies color transformations to the mirrored region based on color_map
    """
    for r, c in mirrored_region:
        output_grid[r,c] = input_grid[r,c]

def transform(input_grid):
    """
    Applies the transformation to the input grid.
    """
    output_grid = np.copy(input_grid)
    objects = get_objects(input_grid)

    for color, obj in objects:
        # 1. Object Partitioning (Simplified: Using bounding box for now)
        rows, cols = zip(*obj)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        # Create a mask for the current object
        object_mask = np.zeros_like(input_grid, dtype=bool)
        for r, c in obj:
            object_mask[r, c] = True

        # 2. & 3. Selective Mirroring/Inversion (Simplified: Inverting within the bounding box)
        # Determine the center of each cluster and try to expand around it
        center_row = (min_row + max_row) // 2
        center_col = (min_col + max_col) // 2


        # Calculate distances of each point to the center
        for row,col in obj:
            dr, dc = abs(row - center_row), abs(col - center_col)
            if row < center_row and col < center_col: # top left
              for i in range(-1,-1-dr,-1):
                for j in range(-1,-1-dc,-1):
                  if 0 <= row+i < input_grid.shape[0] and 0 <= col + j < input_grid.shape[1]:
                    output_grid[row+i,col+j] = input_grid[row,col]
            elif row < center_row and col >= center_col: # top right
              for i in range(-1,-1-dr,-1):
                for j in range(1,1+dc):
                  if 0 <= row+i < input_grid.shape[0] and 0 <= col + j < input_grid.shape[1]:
                    output_grid[row+i,col+j] = input_grid[row,col]            
            elif row >= center_row and col < center_col: # bottom left
              for i in range(1,1+dr):
                for j in range(-1,-1-dc,-1):
                  if 0 <= row+i < input_grid.shape[0] and 0 <= col + j < input_grid.shape[1]:
                    output_grid[row+i,col+j] = input_grid[row,col]
            elif row >= center_row and col >= center_col: # bottom right
              for i in range(1,1+dr):
                for j in range(1,1+dc):
                  if 0 <= row+i < input_grid.shape[0] and 0 <= col + j < input_grid.shape[1]:
                    output_grid[row+i,col+j] = input_grid[row,col]
        
        mirrored_region = set()
        for r in range(min_row - (center_row-min_row), center_row + 1):
          for c in range(min_col - (center_col-min_col),center_col+ 1):
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
              mirrored_region.add((r,c))
        for r in range(min_row - (center_row-min_row), center_row + 1):
          for c in range(center_col,max_col+ (max_col-center_col)+1):
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
              mirrored_region.add((r,c))
        for r in range(center_row, max_row + (max_row-center_row)+1):
          for c in range(min_col - (center_col-min_col),center_col+ 1):
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
              mirrored_region.add((r,c))
        for r in range(center_row, max_row + (max_row-center_row)+1):
          for c in range(center_col,max_col+ (max_col-center_col)+1):
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
              mirrored_region.add((r,c))

        apply_color_mapping(mirrored_region,input_grid, output_grid)
            
    return output_grid