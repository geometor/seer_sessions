"""
1.  **Identify Objects:** Find all contiguous regions of green (3) pixels and red (2) pixels in the input grid. These are considered distinct objects.

2.  **Move and Stack Green Objects:**
    *   For each column containing green pixels:
        *   Find the lowest row index (`r`) with a green pixel in that column.
        *   Starting from row `r` and moving upwards, change any empty (0) cells to green (3).
        *   Continue until the top of the grid is reached or a cell is encountered with a green object in it already.

3.  **Position Red Object:**
    *    Identify columns that contain green.
    *    Find the highest row index with a green pixel (across all columns with a green pixel)
    *   Position the red object directly *above* the highest row that contains green, maintaining the original shape of the red object. This means the lowest row of the red object will be one row above the highest green row.
    *    Ensure that red does not overlap any green pixels. Skip the red object if it does not fit above the green.

4.  **Implicit Fill:** Any remaining cells in the output that haven't been filled by the above steps remain empty (0).
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))
    return objects

def move_and_stack_green_objects(green_objects, output_grid):
    """Moves and stacks green objects upwards."""

    # Get all columns that contain any green pixel
    green_cols = sorted(list(set([c for _, c in np.argwhere(output_grid == 3)])))

    for col in green_cols:
        # Find the lowest row containing green in this column in the *original* objects
        lowest_row = -1
        for green_object in green_objects:
          for r,c in green_object:
            if c == col:
              lowest_row = max(lowest_row, r)
        
        # Stack green upwards from the lowest row
        if lowest_row != -1:  # Ensure there was green in this column
            target_row = 0
            for r in range(lowest_row, -1, -1):
                if output_grid[r, col] == 0:
                  output_grid[r,col] = 3
    return

def position_red_object(red_object, output_grid):
    """Positions the red object above the highest green row, without overlapping."""
   
    # Find the highest green row
    green_rows = [r for r, c in np.argwhere(output_grid == 3)]
    highest_green_row = min(green_rows) if green_rows else output_grid.shape[0] # Default to bottom if no green
    
    # Determine red object height
    red_object_height = max(r for r,_ in red_object) - min(r for r, _ in red_object) + 1
    
    # Calculate target top row for red object
    target_top_row = highest_green_row - red_object_height
    
    # Check if red object fits
    if target_top_row < 0:
        return  # Red object doesn't fit

    # find original top row
    min_row = min(r for r,_ in red_object)

    # Calculate offset to maintain shape
    row_offset = target_top_row - min_row

    # Place the red object
    for r, c in red_object:
        if 0 <= r + row_offset < output_grid.shape[0]:
            output_grid[r + row_offset, c] = 2

def transform(input_grid):
  # initialize output_grid
  output_grid = np.zeros_like(input_grid)

  # find green objects
  green_objects = find_objects(input_grid, 3)

  # pre-fill output grid to account for stacking
  for green_object in green_objects:
    for r,c in green_object:
      output_grid[r,c] = 3

  # move and stack green
  move_and_stack_green_objects(green_objects, output_grid)
  
  # find red objects
  red_objects = find_objects(input_grid, 2)

  # position red
  for red_object in red_objects:
    position_red_object(red_object, output_grid)

  return output_grid