# b775ac94 • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all distinct clusters of contiguous, non-white pixels in the input grid.  Each cluster is an object.

2.  **Conditional Transformation:**
    * If an object's color is blue AND the input object is not found in the output, change the object's color to green.
    * Otherwise reconstruct the object in the output grid at the original location, with the original attributes.

3.  **Reconstruct:** Create an output grid with the same dimensions as the input. Place transformed and unchanged objects in their corresponding positions.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects (contiguous non-zero pixels) in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] == 0:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on object properties and presence in output.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Start with a copy

    input_objects = find_objects(input_grid)

    for obj in input_objects:
        # Get object properties (color)
        first_pixel_color = input_grid[obj[0]]

        # Conditional Transformation
        if first_pixel_color == 1:  # Blue object
          is_present = False # initialize
          for row, col in obj:  # check pixels
            if output_grid[row][col] == 1:
                is_present = True
                break
          if not is_present: # If blue and not in the place it started
            for row, col in obj:
                output_grid[row, col] = 3  # Change to green
        #else the object is copied by virtue of initializing with copy

    return output_grid.tolist()
```
