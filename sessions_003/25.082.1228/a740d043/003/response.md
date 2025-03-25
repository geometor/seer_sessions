```python
"""
1.  **Identify Objects:** Scan the input grid and identify all contiguous rectangular regions that are *not* the color blue (value 1).

2.  **Extract Shapes:** Extract each of these identified non-blue rectangular shapes.  Record the original position of each extracted shape.

3.  **Remove Blue:** Within each extracted shape, replace any blue pixels (value 1) with 0.

4.  **Construct Output:** Create a new output grid.
    *   Iterate through columns of the *input* grid.
    *   For each input column, iterate through the *extracted shapes*.
    *   If a shape was found at least partially in the current column, copy it's values, by column, to the output.
        * if an output cell already has a non-zero value, do not overwrite it.
    * Remove any empty rows and columns.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous non-blue regions in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 1:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def extract_shape(grid, object_coords):
    """
    Extracts the rectangular shape defined by object_coords and records its original position.
    """
    min_r = min(r for r, _ in object_coords)
    max_r = max(r for r, _ in object_coords)
    min_c = min(c for _, c in object_coords)
    max_c = max(c for _, c in object_coords)
    
    shape = grid[min_r:max_r + 1, min_c:max_c + 1].copy()
    # Replace 1s (blue) with 0s (background)
    shape[shape == 1] = 0
    return shape, (min_r, min_c)

def remove_padding(grid):
    """Removes rows and columns that are all zeros from the edges."""
    if grid.size == 0:  # Handle empty grids
        return grid
    # Remove zero rows from top
    while grid.shape[0] > 0 and np.all(grid[0] == 0):
        grid = grid[1:]
    # Remove zero rows from bottom
    while grid.shape[0] > 0 and np.all(grid[-1] == 0):
        grid = grid[:-1]
    # Remove zero columns from left
    while grid.shape[1] > 0 and np.all(grid[:, 0] == 0):
        grid = grid[:, 1:]

    # Remove zero colums from right
    while grid.shape[1] > 0 and np.all(grid[:, -1] == 0):
        grid = grid[:, :-1]
        
    return grid

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find all non-blue objects
    objects = find_objects(input_grid)
    
    # Extract the shapes and their original positions
    extracted_shapes = [extract_shape(input_grid, obj) for obj in objects]

    # Initialize an output grid with zeros.  Use maximum possible dimensions initially, trim later.
    max_height = input_grid.shape[0] #max(r for shape, (r,c) in extracted_shapes) + 1 #input_grid.shape[0]
    max_width = input_grid.shape[1] #max(c for shape, (r,c) in extracted_shapes) + 1 #input_grid.shape[1]
    
    output_grid = np.zeros((max_height, max_width), dtype=int)


    # Iterate through the columns of the INPUT grid
    for input_col in range(input_grid.shape[1]):
        # For each column, iterate through the extracted shapes.
      for shape, (start_row, start_col) in extracted_shapes:
            shape_height, shape_width = shape.shape
            
            #check if shape exists in this column
            if start_col <= input_col < start_col + shape_width:
                #copy column to output, only if output is 0
              output_col = input_col - start_col #relative col index within shape                
              for i in range(shape_height):
                if output_grid[start_row + i, input_col] == 0:
                    output_grid[start_row + i,input_col] = shape[i,output_col]

    # Remove zero padding from the edges
    output_grid = remove_padding(output_grid)
    
    return output_grid.tolist()
```