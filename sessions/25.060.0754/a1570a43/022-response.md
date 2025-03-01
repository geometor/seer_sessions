# a1570a43 • 022 • example_4 • investigate_coder

---
```python
"""
Identify the red object, and shift the uppermost pixel of the red object to its adjacent left position.
"""

import numpy as np

def find_objects(grid, color):
    # Find all objects of a specific color in the grid.
    objects = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(row, col, current_object):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        
        # Explore adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find red objects
    red_objects = find_objects(input_grid, 2)
    
    # Iterate through each red object
    for red_object in red_objects:
        # Find the uppermost pixel of the red object
        if red_object:  # Check if the object is not empty
            uppermost_pixel = min(red_object, key=lambda x: x[0])

            # Shift the uppermost pixel to the left
            new_row = uppermost_pixel[0]
            new_col = uppermost_pixel[1] - 1
            
            if 0<= new_col < output_grid.shape[1]: #bounds check
                output_grid[uppermost_pixel[0], uppermost_pixel[1]] = 0    # clear the original
                output_grid[new_row,new_col] = 2          # set pixel to the left
            
    return output_grid
```
