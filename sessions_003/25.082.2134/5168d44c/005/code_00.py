"""
1.  **Identify Objects:** Locate all contiguous regions (objects) of green (3) and red (2) pixels in the input grid.
2.  **Move Green Objects:**
    *   For each green object, move it upwards.
    *   Fill all empty (0) cells directly above the green object's original position with green (3).
    *    If, during the upward movement, a green object encounters another green object, they merge into a single, larger green object. Continue until no empty spaces above
3.  **Move Red Objects:**
      * Determine the lowest row occupied by any green pixels in the grid after the green object movement
      * Find the topmost row previously occupied by the red object.
      * Position the red object starting one row below the lowest green row.
      * If there are no green objects, leave the red object in its original position.
4.  **Fill Remaining Spaces:** Any remaining empty cells in the output grid should be filled with 0.
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

def move_green_objects(green_objects, output_grid):
    """Moves green objects upwards, filling blank cells and merging."""
    for green_object in green_objects:
        # Get columns occupied by the green object
        cols = [c for _, c in green_object]
        min_col = min(cols)
        max_col = max(cols)
        
        # Find the highest available row for each column
        for c in range(min_col, max_col + 1):
            target_row = 0
            for r in range(output_grid.shape[0]):
                if output_grid[r, c] == 0:
                    target_row = r
                else:
                    break

            # Fill the column up to target_row with green
            for r in range(target_row, -1, -1):
                if any((r,c) in go for go in green_objects):
                    break
                if output_grid[r,c] == 0:
                  output_grid[r,c] = 3
                
        # place original object        
        for r,c in green_object:
          if output_grid[r,c] == 0:
            output_grid[r,c] = 3
    return

def move_red_object(red_object, output_grid):
    """Positions the red object below the lowest green row."""
    
    #find lowest green row
    green_rows = [r for r, c in np.argwhere(output_grid == 3)]
    lowest_green_row = max(green_rows) if green_rows else -1
    
    # find original top row
    min_row = min(r for r,_ in red_object)
    
    # calculate offset to maintain shape
    row_offset = lowest_green_row + 1 - min_row

    # Place the red object
    for r, c in red_object:
      if 0 <= r + row_offset < output_grid.shape[0]:
        output_grid[r + row_offset, c] = 2

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find green objects
    green_objects = find_objects(input_grid, 3)

    # move green objects
    move_green_objects(green_objects, output_grid)
    
    # find red objects
    red_objects = find_objects(input_grid, 2)
    
    # move red object
    for red_object in red_objects:
        move_red_object(red_object, output_grid)


    return output_grid