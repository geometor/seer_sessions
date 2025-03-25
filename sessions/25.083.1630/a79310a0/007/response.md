```python
"""
The program identifies contiguous blocks of azure (8) pixels in the input grid. For each
azure object, it creates a red (2) object with the same dimensions and shape. The
red objects are centered vertically and horizontally in the output grid. If a red
object cannot be perfectly centered, it's placed closer to the top-left. The original
azure objects are removed from the output.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of a specified color."""
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
            if not visited[row, col] and grid[row, col] == color:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_object_dimensions(obj):
    """Calculates the height and width of an object."""
    min_row = min(point[0] for point in obj)
    max_row = max(point[0] for point in obj)
    min_col = min(point[1] for point in obj)
    max_col = max(point[1] for point in obj)
    return max_row - min_row + 1, max_col - min_col + 1

def calculate_center_placement(output_grid_shape, object_height, object_width):
    """Calculates the top-left placement coordinates for centering, adjusting for bounds."""
    center_row = output_grid_shape[0] // 2
    center_col = output_grid_shape[1] // 2
    placement_row = center_row - (object_height // 2)
    placement_col = center_col - (object_width // 2)

    # Adjust placement to ensure the object fits within the grid boundaries
    if placement_row < 0:
        placement_row = 0
    elif placement_row + object_height > output_grid_shape[0]:
        placement_row = output_grid_shape[0] - object_height

    if placement_col < 0:
        placement_col = 0
    elif placement_col + object_width > output_grid_shape[1]:
        placement_col = output_grid_shape[1] - object_width
    
    return placement_row, placement_col
    
def get_object_shape(obj):
    """Gets the shape of the object relative to its top-left corner."""
    min_row = min(r for r, c in obj)
    min_col = min(c for r, c in obj)
    return [(r - min_row, c - min_col) for r, c in obj]

def transform(input_grid):
    # Initialize output_grid with zeros (white)
    output_grid = np.zeros_like(input_grid)

    # Find azure objects
    azure_objects = find_objects(input_grid, 8)

    # Create and position red objects
    for obj in azure_objects:
        # Get object dimensions
        object_height, object_width = get_object_dimensions(obj)

        # Calculate placement for centering
        placement_row, placement_col = calculate_center_placement(output_grid.shape, object_height, object_width)

        # Get the object's shape
        object_shape = get_object_shape(obj)
        
        #remove original
        for row, col in obj:
          output_grid[row,col] = 0

        # Create red object and place in center
        for row_offset, col_offset in object_shape:
            new_row = placement_row + row_offset
            new_col = placement_col + col_offset

            # Check bounds
            if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                output_grid[new_row, new_col] = 2

    return output_grid
```