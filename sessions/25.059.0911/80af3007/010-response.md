# 80af3007 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Gray Regions:** Examine the input grid and locate all isolated regions of gray (5) pixels. A region is defined as a group of orthogonally connected gray pixels.
2.  **Extract Relative Coordinates:** For each of the three large isolated gray shapes determine a top-left corner.
3.  **Create Sub-grid:** Create a new output grid of 9x9
4.  **Translate Gray Regions:** For each pixel in the top-left coordinates, place gray pixels onto the new sub-grid. Note, there is one pixel between each placement.
5.  **Place the lower shape:** Note that the gray shape that appears lowest in the image is placed in the middle of the sub-grid.
6.  **Finalize:** The resulting 9x9 grid is the output.
"""

import numpy as np

def find_objects(grid, color):
    """Finds connected regions of a specific color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects


def get_top_left(obj):
     """Returns the top-left coordinate of an object."""
     min_row = min(p[0] for p in obj)
     min_col = min(p[1] for p in obj)
     return (min_row,min_col)


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)

    # Find gray objects
    gray_objects = find_objects(input_grid, 5)
    
    # Sort gray objects by lowest y coordinate (reversed row index, so -row)
    gray_objects_sorted = sorted(gray_objects, key=lambda obj: -max(p[0] for p in obj))

    #Get the reference positions, place middle shape first
    reference_objects = [gray_objects_sorted[0], gray_objects_sorted[1], gray_objects_sorted[2]]

    #Relative object placements
    coords = [(4,4),(1,1),(1,7)]
        
    #Place the objects in output grid
    for i in range(len(reference_objects)):

        top_left = get_top_left(reference_objects[i])
        output_grid[coords[i][0],coords[i][1]] = 5

        #draw 3x2 shape using relative positioning
        if i == 0: #middle object
            output_grid[coords[i][0]-1,coords[i][1]-1] = 5
            output_grid[coords[i][0]-1,coords[i][1]+1] = 5
            output_grid[coords[i][0]+1,coords[i][1]-1] = 5
            output_grid[coords[i][0]+1,coords[i][1]+1] = 5
        else: #side objects
            output_grid[coords[i][0]+1,coords[i][1]-1] = 5
            output_grid[coords[i][0]+1,coords[i][1]+1] = 5
            output_grid[coords[i][0]-1,coords[i][1]-1] = 5
            output_grid[coords[i][0]-1,coords[i][1]+1] = 5
        

    return output_grid
```
