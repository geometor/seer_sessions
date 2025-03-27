```python
"""
1.  **Identify** the location of all orange (7) pixels in the input grid.
2.  **Iterate** from top to bottom, at each '7':
    1.  **Insert** the series "8 7" above the current '7' to the top of the grid.
    2.  **Shift** down the bottom row '7' from the bottom to match inserted lines.
    3.  **Terminate** if no more 7's
"""

import numpy as np

def get_objects(grid, color):
    objects = []
    visited = set()

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
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
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find orange (7) pixels
    orange_pixels = get_objects(input_grid, 7)
    if not orange_pixels:
        return output_grid
    orange_pixels = orange_pixels[0] # expecting single object
    orange_pixels.sort()
    
    insertions = 0
    for row, col in orange_pixels:
        r = row + insertions
        
        if r-1 < 0:
            continue

        output_grid[1:r+1, :] = output_grid[0:r, :]
        output_grid[0,:] = 0 #clear top row
        
        output_grid[0, col] = 7
        
        if (col - 1) >= 0:
            output_grid[0, col-1] = 8
        
        insertions += 1
        
    return output_grid
```