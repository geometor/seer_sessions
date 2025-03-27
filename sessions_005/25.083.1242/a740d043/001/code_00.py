"""
1.  **Identify Non-Blue Pixels:** Scan the input grid and identify all pixels that are not blue (value 1).
2.  **Extract Non-Blue Shapes:** Group contiguous non-blue pixels into distinct shapes.
3. **Remove the background:** Remove all blue pixels.
4.  **Create Output Grid:** Construct a new grid. The dimensions of the new grid
    are determined by the size and number of non-blue pixel groups found.
5.  **Populate Output:** Place the extracted non-blue shapes into the output
    grid. There are potentially multiple groups of pixels - stack them
    vertically. Fill the spaces between the pixel groups with white (0).
6. Iterate until all pixel groups are arranged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of non-blue pixels in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
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
        current_object.append((r, c, grid[r,c]))
        # Check adjacent cells (up, down, left, right)
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)

    return objects

def transform(input_grid):
    """
    Transforms the input grid by extracting non-blue shapes and arranging them in a new grid.
    """
    input_grid = np.array(input_grid)

    # Find non-blue objects
    objects = find_objects(input_grid)

    # Calculate output grid dimensions
    max_width = 0
    total_height = 0
    
    for obj in objects:
      height = max(y for y,x,_ in obj) - min(y for y,x,_ in obj) + 1
      width = max(x for y,x,_ in obj) - min(x for y,x,_ in obj) + 1      
      max_width = max(max_width, width)
      total_height += height

    # Initialize output grid
    output_grid = np.zeros((total_height, max_width), dtype=int)

    # Populate the output grid.
    current_row = 0
    for obj in objects:
        #find width and height of object.
        min_row = min(r for r, c, _ in obj)
        min_col = min(c for r, c, _ in obj)
        
        for r, c, val in obj:
          output_grid[r - min_row + current_row, c - min_col] = val

        # move down to place next object.
        current_row += (max(r for r, c, _ in obj) - min_row + 1)

    return output_grid.tolist()