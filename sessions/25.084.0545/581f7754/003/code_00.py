"""
The transformation rule involves inverting each object within the input grid and placing them in the output grid. The objects are defined by contiguous regions of the same color.  The inversion is performed by reversing both the rows and columns *within the bounding box* of each object. If there is a conflict in color when adding inverted grids to the output, use the lower color value.
"""

import numpy as np

def get_objects(grid):
    """
    Iterative version of get_objects using a stack.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                grid_value = grid[row][col]
                current_object = set()
                stack = [(row, col)]

                while stack:
                    r, c = stack.pop()
                    if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != grid_value:
                        continue
                    visited.add((r, c))
                    current_object.add((r, c))
                    stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])

                objects.append((grid_value, current_object))
    return objects

def transform(input_grid):
    # Initialize output_grid with the same dimensions and filled with zeros
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Get objects from the input grid
    objects = get_objects(input_grid.tolist()) # convert to list for compatibility with iterative get_objects
    
    # Process and reflect each object
    for value, obj in objects:
      # Find bounding box
      min_r = min([r for r, c in obj])
      max_r = max([r for r, c in obj])
      min_c = min([c for r, c in obj])
      max_c = max([c for r, c in obj])

      # Create a temporary grid for the object
      temp_grid = np.full((max_r - min_r + 1, max_c - min_c + 1), 0)
      for r, c in obj:
        temp_grid[r - min_r][c - min_c] = value
      
      # Invert object rows and cols *within its bounding box*
      inverted_grid = temp_grid[::-1, ::-1]
      
      # Place the inverted object into the output grid
      for r in range(inverted_grid.shape[0]):
          for c in range(inverted_grid.shape[1]):
              new_r = min_r + r
              new_c = min_c + c
              # Ensure we're within output_grid bounds (should always be true, but good practice)
              if 0 <= new_r < rows and 0 <= new_c < cols:
                  # Apply the rule: if the output cell is empty (0) OR the new value is smaller, update
                  if (output_grid[new_r][new_c] == 0 or output_grid[new_r][new_c] > inverted_grid[r][c]) and inverted_grid[r][c] != 0:
                      output_grid[new_r][new_c] = inverted_grid[r][c]

    return output_grid.tolist()