```python
"""
Extracts colored objects from the input grid, preserves their shapes, and arranges them in a new grid from top-left to bottom-right, based on the original top-left position of each object in the input grid. Objects are placed in rows, and if an object doesn't fit in the current row, it moves to the next row.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and extracts contiguous blocks of non-zero colored pixels.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj = []
                dfs(r, c, grid[r, c], obj)
                if obj:
                    objects.append(obj)
    return objects

def object_dimensions(obj):
    """
    Calculates the height and width of an object.
    """
    rows, cols = zip(*obj)
    height = max(rows) - min(rows) + 1
    width = max(cols) - min(cols) + 1
    return height, width

def object_top_left(obj):
    """
    Returns the top-left coordinates (row, col) of an object.
    """
    return min(r for r, _ in obj), min(c for _, c in obj)
    

def transform(input_grid):
    """
    Transforms the input grid by extracting, preserving, and arranging colored objects.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Identify and Extract objects
    objects = get_objects(input_grid)

    # Order the objects by top-left corner (row, then column)
    ordered_objects = sorted(objects, key=object_top_left)

    # Initialize output grid parameters
    output_rows = 0
    output_cols = 0
    current_row = 0
    current_col = 0
   
    object_data = [] # store (object, height, width, top_left_row, top_left_col)
    
    for obj in ordered_objects:
        height, width = object_dimensions(obj)
        
        # if object will exceed current row length
        if current_col + width > output_cols:
            # update output size
            output_cols = max(output_cols, current_col + width) # extend width if needed
            current_row += height if current_col > 0 else 0  # only start new row if not first object
            current_col = 0 # reset to left
          
        # store for placement
        object_data.append((obj, height, width, current_row, current_col))
        current_col += width    # move horiz position by width

    # compute the final size
    max_row = 0
    for obj, height, width, top_left_row, top_left_col in object_data:
      max_row = max(max_row, top_left_row+height)
      
    output_grid = np.zeros((max_row, output_cols), dtype=int)

    # place objects in grid
    for obj, height, width, top_left_row, top_left_col in object_data:
      # fill object into grid at computed position
      for r,c in obj:
        row_offset = r - object_top_left(obj)[0]
        col_offset = c - object_top_left(obj)[1]
        output_grid[top_left_row + row_offset, top_left_col + col_offset] = input_grid[r,c]

    return output_grid.tolist()
```