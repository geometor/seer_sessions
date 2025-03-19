# 776ffc46 • 008 • refine_coder

---
```python
"""
The input grid contains gray borders, red "plus" shapes, and blue "plus" shapes. The transformation rule
involves changing the color of *some* blue plus shapes to red, but only under specific conditions.
Based on analyzing all training examples, a blue plus shape is changed to red only if it's the *top-most* blue plus shape within a gray-bordered region. If there are two or more blue plus shapes at the same minimal y-coordinate, the left-most one is changed to red.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds all connected components of a specified color in the grid.
    Returns a list of lists, where each inner list contains the coordinates of a connected object.
    """
    objects = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def find_plus_shapes(grid, color):
    """
    Finds all "plus" shaped objects of a specified color in the grid.
    Returns a list of center coordinates of the plus shapes.
    """
    plus_centers = []
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if (grid[r, c] == color and
                grid[r - 1, c] == color and
                grid[r + 1, c] == color and
                grid[r, c - 1] == color and
                grid[r, c + 1] == color):
                plus_centers.append((r, c))
    return plus_centers

def is_inside(point, region):
    """Checks if a point is inside a region (list of points)."""
    return point in region

def transform(input_grid):
    """
    Transforms the input grid by changing the top-most blue plus shape within each gray border to red.
    """
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find all gray objects (borders).
    gray_objects = find_objects(input_grid, 5)
    
    # Find all blue plus shapes.
    blue_plus_centers = find_plus_shapes(input_grid, 1)

    # Iterate through each gray object.
    for gray_object in gray_objects:
        # Find blue plus shapes inside the current gray object.
        blue_plus_inside = [center for center in blue_plus_centers if any(is_inside((r,c), gray_object) for r in range(center[0]-1, center[0]+2) for c in range(center[1]-1, center[1]+2))]
        
        # Find the top-most blue plus shape(s) inside the gray border.
        if blue_plus_inside:
            min_row = min(center[0] for center in blue_plus_inside)
            top_most_centers = [center for center in blue_plus_inside if center[0] == min_row]

            # If there are multiple top-most, select the left-most.
            left_most_center = min(top_most_centers, key=lambda x: x[1])
            center_r, center_c = left_most_center
            
            # Change the selected blue plus shape to red.
            output_grid[center_r, center_c] = 2
            output_grid[center_r - 1, center_c] = 2
            output_grid[center_r + 1, center_c] = 2
            output_grid[center_r, center_c - 1] = 2
            output_grid[center_r, center_c + 1] = 2

    return output_grid
```
