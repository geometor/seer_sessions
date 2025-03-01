# a1570a43 • 024 • refine_coder

---
```python
"""
Identify the red object(s) within the grid. For each red object, examine each pixel. If a red pixel is adjacent to a white (0) pixel, and moving it one position to the left will place it within the bounds of the grid, then shift that red pixel one position to the left. Only those red pixels adjacent to white pixels on any side (up, down, left, right) are moved.
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

def get_adjacent_colors(grid, row, col):
    """Returns a set of colors adjacent to the given cell (up, down, left, right)."""
    adjacent_colors = set()
    rows, cols = grid.shape
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Only check left, right, up, down
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            adjacent_colors.add(grid[r, c])
    return adjacent_colors

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find red objects
    red_objects = find_objects(input_grid, 2)
    
    # Iterate through each red object and each pixel in object
    for red_object in red_objects:
        for row, col in red_object:
            # Check if the red pixel is adjacent to a white pixel
            if 0 in get_adjacent_colors(input_grid, row, col):
                # Calculate the new position (one step to the left)
                new_col = col - 1

                # Check if the new position is within the grid bounds
                if 0 <= new_col < output_grid.shape[1]:
                    # Move the red pixel to the new position
                    output_grid[row, col] = 0           # Clear original position
                    output_grid[row, new_col] = 2       # Set new position to red

    return output_grid
```
