# 5582e5ca • 018 • refine_coder

---
```python
"""
1.  **Examine the input and output grids.** Identify all distinct objects (contiguous regions of the same color).

2.  **Determine the presence of gray and magenta** in both input and output grids.

3.  **Check for Flood Fill**: Determine if output grid is flood filled (all one color)

4.  **Gray Rule**: If the input grid contains any gray pixels, flood fill the output grid with gray.

5.  **Magenta Flood Fill Rule**: Otherwise, if the output is flood filled with magenta, then flood fill the output with magenta.

6.  **3x3 Magenta Region**: If the output grid has 3x3 regions of magenta, then copy the input, but add a 3x3 magenta region in top left. Note: requires input grid to be at least 3x3.

7.  **Otherwise:** (This step is added as a default to cover edge cases). Copy input to output.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of the same color in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if object_pixels:
                    objects.append(object_pixels)
    return objects

def transform(input_grid):
    # initialize output_grid to copy of input
    output_grid = np.copy(input_grid)

    # Find objects in the input grid
    input_objects = find_objects(input_grid)

    # Check if input contains gray (5)
    input_has_gray = any(input_grid[obj[0]] == 5 for obj in input_objects)
    if input_has_gray:
      output_grid[:] = 5
      return output_grid
      
    # Check if input contains magenta (6)
    input_has_magenta = any(input_grid[obj[0]] == 6 for obj in input_objects)

    # Check if output is flood filled
    unique_colors = np.unique(output_grid)
    is_flood_fill = len(unique_colors) == 1
    if is_flood_fill:
      if unique_colors[0] == 6:
        output_grid[:] = 6
        return output_grid

    # Check from training example 2 for 3x3 magenta
    magenta_present = False
    if output_grid.shape[0] >=3 and output_grid.shape[1] >= 3:
        
        # Create 3x3 magenta check
        for r in range(output_grid.shape[0] - 2):
            for c in range(output_grid.shape[1] - 2):
                if all([output_grid[r+i,c+j] == 6 for i in range(3) for j in range(3)]):
                    magenta_present = True
                    break
    
        if magenta_present:
            #create a magenta region
            output_grid[:3, :3] = 6
            return output_grid

    return output_grid
```
