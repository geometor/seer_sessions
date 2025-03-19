# 80af3007 • 012 • refine_coder

---
```python
"""
1.  **Identify Gray Objects:** Examine the input grid and identify the three distinct gray (color 5) objects.  There are three shape types: a "cross" shape, a "T" shape, and an "I" shape.

2.  **Determine Vertical Order:** Sort the three gray objects based on their vertical position in the input grid. The object that appears *lowest* in the input grid will be considered the "middle" object. The object appearing highest is the "top" object.

3.  **Create Output Grid:** Create a 9x9 output grid filled with black (color 0).

4.  **Replicate and Arrange:** Replicate the objects based on the "middle object", placing the copies in the following positions on the 9x9 grid. The layout is always this grid:

```
[top_left | top_middle | top_right]
[mid_left |   middle   | mid_right]
[bot_left | bot_middle | bot_right]
```

Place a copy of the appropriate object (cross, T, or I) in each position. The "middle" object is placed in the center (4,4). The object that appears *highest* in the input grid is used for the "top" positions.

5. **Shape Preservation:** Ensure each copy retains the original shape (cross, T, or I).

6. **Output:** The resulting 9x9 grid is the final output.
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
    return (min_row, min_col)

def get_object_shape(obj):
    """Classifies the shape of an object as 'cross', 'T', or 'I'."""
    coords = sorted(obj)
    rows = [p[0] for p in coords]
    cols = [p[1] for p in coords]
    
    if len(coords) == 5:
        #check middle for cross, T and I
        row_counts = {r: rows.count(r) for r in set(rows)}
        col_counts = {c: cols.count(c) for c in set(cols)}
        #check for cross
        if 3 in row_counts.values() and 3 in col_counts.values():
            return 'cross'
        #check for T
        elif 3 in row_counts.values() and 1 in row_counts.values():
            return 'T'
    elif len(coords) == 3: # Check for I
        if len(set(rows)) == 1 or len(set(cols)) == 1:
                return 'I'


    return 'unknown'
    

def draw_shape(grid, shape_type, top_left):
     """Draws the specified shape onto the grid starting at the top_left coordinate."""
     row, col = top_left
     if shape_type == 'cross':
          grid[row, col] = 5
          grid[row-1, col] = 5
          grid[row+1, col] = 5
          grid[row, col-1] = 5
          grid[row, col+1] = 5
     elif shape_type == 'T':
          grid[row, col] = 5
          grid[row-1, col] = 5
          grid[row+1, col] = 5
          grid[row, col-1] = 5
          grid[row, col+1] = 5
     elif shape_type == 'I':
          grid[row, col] = 5
          grid[row, col-1] = 5
          grid[row, col+1] = 5
     return grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)

    # Find gray objects
    gray_objects = find_objects(input_grid, 5)
    
    # Sort gray objects by lowest y coordinate (reversed row index)
    gray_objects_sorted = sorted(gray_objects, key=lambda obj: -max(p[0] for p in obj))

    # Get object shapes
    shapes = [get_object_shape(obj) for obj in gray_objects_sorted]

    # Determine object order (top, middle, bottom) based on vertical position
    middle_object_shape = shapes[0]
    top_object_shape = shapes[-1]
    #get bottom object - the one left
    remaining_shapes = [s for s in shapes if s != middle_object_shape and s != top_object_shape]
    bottom_object_shape = remaining_shapes[0]
    
    # Define layout positions
    layout = {
        'top_left': (1, 1), 'top_middle': (1, 4), 'top_right': (1, 7),
        'mid_left': (4, 1), 'middle': (4, 4), 'mid_right': (4, 7),
        'bot_left': (7, 1), 'bot_middle': (7, 4), 'bot_right': (7, 7)
    }
    
    #Place objects
    #place top object
    output_grid = draw_shape(output_grid, top_object_shape, layout['top_left']) #top_left
    output_grid = draw_shape(output_grid, middle_object_shape, layout['top_middle']) #top_middle
    output_grid = draw_shape(output_grid, bottom_object_shape, layout['top_right']) #top_right
    #place mid objects
    output_grid = draw_shape(output_grid, middle_object_shape, layout['mid_left']) #mid_left
    output_grid = draw_shape(output_grid, bottom_object_shape, layout['middle'])  # Middle
    output_grid = draw_shape(output_grid, top_object_shape, layout['mid_right']) #mid_right
    #place bot objects
    output_grid = draw_shape(output_grid, bottom_object_shape, layout['bot_left']) #bot_left
    output_grid = draw_shape(output_grid, top_object_shape, layout['bot_middle']) #bot_middle
    output_grid = draw_shape(output_grid, middle_object_shape, layout['bot_right'])#bot_right

    return output_grid
```
