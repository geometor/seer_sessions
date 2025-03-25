```python
"""
Change connected blue objects to red, starting from the top row and propagating downward, stopping propagation if a new disconnected blue object is encountered.
"""

import numpy as np

def find_contiguous_objects(grid, color):
    """Finds contiguous objects of the specified color in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        """Depth-First Search helper function."""
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        # Explore adjacent cells
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Find blue objects
    blue_objects = find_contiguous_objects(input_grid, 1)
    
    # Keep track of changed pixels to propagate changes downwards
    changed_pixels = set()

    # Iterate through each row
    for row in range(rows):
        for col in range(cols):
            #If pixel is blue
            if output_grid[row,col] == 1:
                #If on first row, always change to red.
                if row == 0:
                    output_grid[row,col] = 2
                    changed_pixels.add((row,col))
                #If not on the first row, check for changed pixel above.
                elif (row - 1, col) in changed_pixels:
                    output_grid[row,col] = 2
                    changed_pixels.add((row, col))
    return output_grid
```