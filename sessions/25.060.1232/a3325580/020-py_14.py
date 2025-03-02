"""
1.  **Identify Objects:** Examine the input grid and identify all contiguous regions of the same color as distinct objects.
2.  **Locate Specific color:** Find the object with color 2 (red).
3. **Determine Height:** calculate the greatest vertical length of the color 2 object.
4.  **Create Output:** Create a new grid that is is `height` tall by 1 cell wide
5. **Fill output** Fill the grid with the color 2 (red).
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_object_height(obj):
     """
     calculate the greatest vertical length of a single object
     """
     rows = [r for r, c in obj]
     return max(rows) - min(rows) + 1

def transform(input_grid):
    # Find all objects in the input grid
    objects = find_objects(np.array(input_grid))

    # Find the red object (color 2)
    red_objects = [obj for obj in objects if input_grid[obj[0][0]][obj[0][1]] == 2]
    
    # if no red object return empty grid
    if not red_objects:
        return np.array([])

    # Find tallest red object
    tallest_red = max(red_objects, key=get_object_height)
    
    # Determine the height of the red object
    height = get_object_height(tallest_red)
    
    # Create an output grid of the determined height, filled with red (2)
    output_grid = np.full((height, 1), 2)

    return output_grid