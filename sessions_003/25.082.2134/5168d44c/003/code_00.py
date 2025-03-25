"""
1.  **Identify Objects:** Find all contiguous blocks of red (2) and green (3) pixels. Treat each contiguous block as a single object.
2.  **Green Object Movement:** Move each green object upwards.
    *   The green object will fill any available blank (0) cells directly *above* its initial row.
    *   If another green object is above this, it will merge.
3.  **Red Object Movement:** Move the red object downwards.
    *  Determine the top row of the red object in the original input.
    *   Shift the entire red object down such that the top of the red object is one row below the original top row.
    *   If this movement would cause a collision with another non-blank (non-0) pixel, do not move the red object.
4. The output grid's empty spaces are filled with 0.
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

def move_green_object(green_object, output_grid):
    """Moves a single green object upwards, filling blank cells above."""
    min_row = min(r for r, _ in green_object)
    max_col = max(c for _, c in green_object)
    min_col = min(c for _, c in green_object)
    
    # Determine the highest possible row to move the object to
    target_row = 0
    for r in range(min_row -1, -1, -1):
        can_move = True
        for c in range(min_col, max_col + 1):
            if output_grid[r,c] != 0 and not any((r,c) in go for go in find_objects(output_grid,3)):
                can_move = False
                break
        if can_move:
            target_row = r
        else:
            break

    # Move the object
    for r, c in green_object:
        row_offset = r - min_row
        output_grid[target_row + row_offset, c] = 3
        
    return

def move_red_object(red_object, output_grid, original_grid):
    """Moves the red object down one row from its original top position."""
    min_row = min(r for r, _ in red_object)
    max_row = max(r for r, _ in red_object)
    max_col = max(c for _, c in red_object)
    min_col = min(c for _, c in red_object)
    
    target_row = min_row + 1

    # check to ensure within bounds
    if target_row > original_grid.shape[0] - (max_row-min_row + 1):
        # cannot perform move
        for r,c in red_object:
            output_grid[r,c] = 2
        return
    
    # Check for collisions
    for r in range(max_row - min_row + 1):
        for c in range(min_col, max_col + 1):
          if (min_row + r,c) in red_object: #ensure checking correct pixel
            if output_grid[target_row + r, c] != 0:
                # Collision detected, do not move
                for row, col in red_object:
                    output_grid[row, col] = 2
                return

    # Move the object
    for r, c in red_object:
        row_offset = r - min_row
        output_grid[target_row + row_offset, c] = 2

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find green objects
    green_objects = find_objects(input_grid, 3)

    # move green objects
    for green_object in green_objects:
      move_green_object(green_object, output_grid)

    # find red objects
    red_objects = find_objects(input_grid, 2)

    # Move red object
    for red_object in red_objects:
        move_red_object(red_object, output_grid, input_grid)

    return output_grid