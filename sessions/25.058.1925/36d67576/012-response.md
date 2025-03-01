# 36d67576 • 012 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find the largest contiguous yellow (4) object.  Also, locate any blue (1) or green (3) objects.

2.  **Modify Yellow Object:**
    *   Insert a blue (1) pixel inside the yellow object, in the second row from the bottom, maintaining the original column.
    *   Insert a green (3) pixel inside the yellow object, in the third row from the top, maintaining the original column.
    *   Add a blue (1) pixel directly above the top row of the rightmost column of the yellow shape.
    *   Add a green(3) pixel directly above the top row of the leftmost column of the yellow shape.
    *   Add a green(3) pixel directly below the bottom row of the leftmost column of the yellow shape.

3. **Conditional Shape (Based on Example 1 - needs generalization):**
    * If a separate green shape exists in the input
      * Add an "L"-shaped object consisting of green(3) and yellow(4) pixels. The "L" should be added such that the rightmost extent is based on the size of the grid, not any of the existing shapes.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.  Improved version.
    Returns a dictionary where keys are colors and values are lists of object coordinates.
    Each object is represented as a dictionary with 'coords' and other properties.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []
        visited.add((row, col))
        coords = [(row, col)]
        coords.extend(dfs(row + 1, col, color))
        coords.extend(dfs(row - 1, col, color))
        coords.extend(dfs(row, col + 1, color))
        coords.extend(dfs(row, col - 1, color))
        return coords

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                coords = dfs(row, col, color)
                if color not in objects:
                    objects[color] = []

                # Store as a dictionary with properties
                obj_dict = {
                    'coords': coords,
                    'top_left': (min(r for r, c in coords), min(c for r, c in coords)),
                    'bottom_right': (max(r for r, c in coords), max(c for r, c in coords))
                }
                objects[color].append(obj_dict)

    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find objects in the input grid (using improved object recognition)
    objects = find_objects(input_grid)

    # Locate the main yellow (4) shape (assuming it's the largest)
    yellow_shapes = objects.get(4, [])
    if yellow_shapes:
      yellow_shape = max(yellow_shapes, key=lambda x: len(x['coords']))
      yellow_coords = yellow_shape['coords']
      
      # Insert a blue (1) pixel inside the yellow object, second row from bottom
      yellow_bottom_row = max(row for row, col in yellow_coords)
      second_bottom_yellow = [(r,c) for r, c in yellow_coords if r == yellow_bottom_row - 1]
      if second_bottom_yellow:
          blue_insert_col = second_bottom_yellow[0][1]
          output_grid[yellow_bottom_row - 1, blue_insert_col] = 1
    
      # Insert green (3) inside, third row from top
      yellow_top_row = min(row for row, col in yellow_coords)
      third_top_yellow = [(r, c) for r, c in yellow_coords if r == yellow_top_row + 2]
      if third_top_yellow:
        green_insert_col = third_top_yellow[0][1]
        output_grid[yellow_top_row + 2, green_insert_col] = 3
      
      # Add blue (1) above rightmost column
      yellow_rightmost_col = max(col for row, col in yellow_coords)
      top_right_yellow = min([(r,c) for r, c in yellow_coords if c == yellow_rightmost_col], key=lambda x: x[0])
      output_grid[top_right_yellow[0]-1, top_right_yellow[1]] = 1

      # Add green (3) above and below leftmost column
      yellow_leftmost_col = min(col for row, col in yellow_coords)
      top_left_yellow = min([(r,c) for r, c in yellow_coords if c == yellow_leftmost_col], key=lambda x: x[0])
      bottom_left_yellow = max([(r,c) for r,c in yellow_coords if c == yellow_leftmost_col], key=lambda x: x[0])

      output_grid[top_left_yellow[0]-1, top_left_yellow[1]] = 3
      output_grid[bottom_left_yellow[0]+1, bottom_left_yellow[1]] = 3

    # Conditional shape (Example 1 generalization attempt)
    green_shapes = objects.get(3, [])
    if green_shapes:
        # Find a suitable location to the right of all existing content
        max_col_used = 0
        for color, objs in objects.items():
          for obj in objs:
            max_col_used = max(max_col_used, obj['bottom_right'][1])

        #find largest green
        largest_green = max(green_shapes, key=lambda x: len(x['coords']))

        start_col = max_col_used + 1  # Start adding the shape one column to the right
        green_right_row = [row for row, _ in largest_green['coords']]
        max_row = max(green_right_row)
        min_row = min(green_right_row)
        output_grid[max_row -1, start_col] = 3
        output_grid[max_row -1, start_col+1] = 4
        output_grid[max_row -1, start_col + 2] = 3
        output_grid[max_row -1, start_col + 3] = 3
        output_grid[min_row +1, start_col] = 3
        output_grid[min_row +1, start_col + 1] = 4
        output_grid[min_row +1, start_col+2] = 3
        output_grid[min_row +1, start_col +3] = 3

    return output_grid
```
