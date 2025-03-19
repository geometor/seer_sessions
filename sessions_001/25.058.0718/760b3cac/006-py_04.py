"""
1.  **Identify Objects:** Locate all contiguous regions (objects) of yellow (color 4) and azure (color 8) pixels in the input grid.
2.  **Preserve Yellow:** Maintain the position and shape of the yellow object(s) in the output grid.
3.  **Stack Azure Above:** Stack the azure-colored objects *at the top of the output grid*. Maintain the original horizontal (column) position of each azure object. Stack them from top to bottom, with the objects that were originally highest being placed at the very top. If two azure objects were on the same row of the input, place the left-most object on top of the other.
4.  **Empty Remainder:** Fill all remaining cells in the grid with black (color 0).
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of a specified color in the grid."""
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        """Depth-First Search to find contiguous pixels."""
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_object_properties(obj):
    """Calculates properties of an object."""
    min_row = min(r for r, c in obj)
    max_row = max(r for r, c in obj)
    min_col = min(c for r, c in obj)
    max_col = max(c for r, c in obj)
    width = max_col - min_col + 1
    height = max_row - min_row + 1
    return (min_row, min_col), (max_row, max_col), width, height

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Initialize output_grid as all black
    output_grid = np.zeros_like(input_grid)

    # Find yellow and azure objects
    yellow_objects = find_objects(input_grid, 4)
    azure_objects = find_objects(input_grid, 8)

    # Preserve yellow objects
    for obj in yellow_objects:
        for r, c in obj:
            output_grid[r, c] = 4

    # get properties for the azure objects and sort by row, then by column
    azure_object_props = []
    for obj in azure_objects:
      azure_object_props.append(get_object_properties(obj))
    
    azure_object_props.sort(key=lambda x: (x[0][0], x[0][1])) # Sort by row, then column

    # Stack azure objects at the top, maintaining original column and stacking order
    current_row = 0
    
    for top_left, bottom_right, width, height in azure_object_props:
        for r in range(height):
            for c in range(width):
                output_grid[current_row + r, top_left[1] + c] = 8  # Use original column (top_left[1])
        current_row += height

    return output_grid