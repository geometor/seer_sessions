# 7447852a • 005 • refine_coder

---
```python
"""
1.  **Identify Red Shapes:** Find all contiguous blocks of red pixels. Consider them as separate objects.
2.  **Connectivity Check:** Determine if a red shape is "connected" – meaning the red pixels are adjacent horizontally or diagonally.
3.  **Shape Type Check** determine if the shape is a "line". A line is defined as a series of horizontally, vertically, or diagonally adjacent pixels of the same color.
4.  **Conditional Transformation:** If a red shape is a connected line:
    *   Change the first red pixel in the line to yellow.
    *   Skip the next red pixel (leave it red).
    *   Change the next red pixel to yellow, and so on, in an alternating pattern from both ends, towards the center of the line.
5.  **Other Shapes:** If the red shape is *not* a connected line, do not perform any transformations. Leave the pixels as they are.
"""

import numpy as np

def find_connected_components(grid, color):
    """Finds connected components of a given color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_component):
        if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
            return
        visited[x, y] = True
        current_component.append((x, y))

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                dfs(x + dx, y + dy, current_component)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if not visited[x, y] and grid[x, y] == color:
                current_component = []
                dfs(x, y, current_component)
                components.append(current_component)
    return components

def is_line(component):
    """Checks if a component is a line (horizontal, vertical, or diagonal)."""
    if len(component) <= 1:
        return True  # Single pixel or empty is considered a line

    # Convert component coordinates to NumPy array for easier manipulation
    coords = np.array(component)
    x_coords = coords[:, 0]
    y_coords = coords[:, 1]

    # Check for horizontal line (all x coordinates are the same)
    if np.all(x_coords == x_coords[0]):
        return True

    # Check for vertical line (all y coordinates are the same)
    if np.all(y_coords == y_coords[0]):
        return True

    # Check for diagonal line (difference between x and y coordinates is constant)
    diffs = x_coords - y_coords
    if np.all(diffs == diffs[0]):  # Top-left to bottom-right diagonal
        return True

    # Check for anti-diagonal (sum of x and y coordinates is constant)
    sums = x_coords + y_coords
    if np.all(sums == sums[0]):  # Top-right to bottom-left diagonal
         return True

    # Check if the differences in x and y coordinates are constant
    dx = np.diff(x_coords)
    dy = np.diff(y_coords)
    
    if np.all(dx == dx[0]) and np.all(dy == dy[0]) and (abs(dx[0]) <=1 and abs(dy[0])<=1):
        return True


    return False
    

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = input_grid.copy()
    red_components = find_connected_components(input_grid, 2)

    for component in red_components:
        if is_line(component):
            # Sort component by x and then y to handle different line orientations
            component.sort(key=lambda p: (p[0], p[1]))
            
            #Apply alternating transformation from both ends of the line.
            for i in range(0, len(component), 2):
                output_grid[component[i]] = 4
            
            component.sort(key=lambda p: (p[0], -p[1]), reverse=True)

            for i in range(0, len(component), 2):
                output_grid[component[i]] = 4


    return output_grid
```
