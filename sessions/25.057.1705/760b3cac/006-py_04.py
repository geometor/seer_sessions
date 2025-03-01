"""
1.  **Identify Objects:** Find all contiguous regions (objects) of pixels with the same color in the input grid.
2.  **Preserve Yellow:** Yellow objects are unchanged.
3.  **Locate Azure Objects:** Identify the azure (color 8) objects.
4. **Extend Azure Columns:** For each azure object, identify the columns occupied by that object's pixels. Within *only* those columns, extend the azure color upwards from the top-most pixel of the original azure object to the top edge of the grid. The original Azure pixels are not changed.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        """Depth-first search to find contiguous pixels."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
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
                    objects.append({"color": color, "pixels": object_pixels})
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)
    
    # Identify azure objects
    azure_objects = [obj for obj in objects if obj['color'] == 8]

    # Extend azure objects upwards within their specific columns
    for obj in azure_objects:
        # Get the columns occupied by the current azure object
        columns = set([pixel[1] for pixel in obj['pixels']])
        
        for col in columns:
            #find top most pixel for this object in this col
            rows_in_col = [pixel[0] for pixel in obj['pixels'] if pixel[1] == col]
            if rows_in_col: #check for empty list from bad object
                top_row = min(rows_in_col)
            
                # Extend azure color upwards in the current column
                for row in range(top_row):
                    output_grid[row, col] = 8

    return output_grid