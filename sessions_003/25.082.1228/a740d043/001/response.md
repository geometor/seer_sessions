```python
"""
1.  **Identify Non-Blue Shapes:** Scan the input grid and identify all contiguous rectangular regions that are *not* the color blue (value 1).
2.  **Extract Shapes:** Extract each of these identified non-blue rectangular shapes.
3. **Remove all zeros at the edges:** Remove all the padding rows or cols with all zero values at top, bottom, right and left.
4.  **Construct Output:** Create a new grid. Place the extracted shapes into this new grid based on the following criteria:
    - maintain the shape and color
    - place shape on the rows in order they appear from top to bottom.
    - remove the blue.
    - Remove all columns with only 0 values.
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
    Extracts the rectangular shape defined by object_coords.
    """
    min_r = min(r for r, _ in object_coords)
    max_r = max(r for r, _ in object_coords)
    min_c = min(c for _, c in object_coords)
    max_c = max(c for _, c in object_coords)
    
    shape = grid[min_r:max_r + 1, min_c:max_c + 1].copy()
    # Replace 1s (blue) with 0s (background)
    shape[shape == 1] = 0
    return shape
    
def remove_padding(grid):
    """Removes rows and columns that are all zeros from the edges."""
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
    
    # Extract the shapes
    extracted_shapes = [extract_shape(input_grid, obj) for obj in objects]

    # Initialize an output grid with zeros
    max_height = sum(shape.shape[0] for shape in extracted_shapes)
    max_width = max(shape.shape[1] for shape in extracted_shapes if shape.size > 0)  # Handle empty shapes
    if not extracted_shapes or max_width==0 :
      return []
        
    output_grid = np.zeros((max_height, max_width), dtype=int)

    # Place extracted shapes into the output grid
    current_row = 0
    for shape in extracted_shapes:
        h, w = shape.shape
        output_grid[current_row:current_row + h, 0:w] = shape
        current_row += h

    # Remove zero padding from the edges
    output_grid = remove_padding(output_grid)
    
    return output_grid.tolist()
```