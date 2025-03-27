```python
"""
Remove gray background pixels. Divide the remaining grid into three vertical panels.
In each panel, find the smallest object. Change the color of the smallest object
based on its panel: top panel to yellow, middle panel to red, and bottom panel
to green if any training input's height modulo 3 is 0 or 1, otherwise black. If
a panel has no objects after gray removal, skip processing that panel.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, object_coords):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        object_coords.append((row, col))
        dfs(row + 1, col, color, object_coords)
        dfs(row - 1, col, color, object_coords)
        dfs(row, col + 1, color, object_coords)
        dfs(row, col - 1, color, object_coords)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                object_coords = []
                dfs(row, col, color, object_coords)
                if object_coords:
                    objects.append((color, object_coords))
    return objects

def transform(input_grid, example_grid_heights=None):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Remove gray background
    output_grid[output_grid == 5] = 0

    # Find objects
    objects = find_objects(output_grid)

    # Divide into three vertical panels
    rows, cols = output_grid.shape
    panel_height = rows // 3
    panels = [
      (0, panel_height),
      (panel_height, 2 * panel_height),
      (2*panel_height, rows)
    ]

    # Determine bottom panel color based on example grid heights
    bottom_panel_color = 0  # Default to black
    if example_grid_heights:
        for height in example_grid_heights:
            if height % 3 in (0, 1):
                bottom_panel_color = 3  # Green
                break

    # Process each panel
    for panel_index, (start_row, end_row) in enumerate(panels):
        panel_objects = []

        # get objects in panel
        for color, coords in objects:
          for row,col in coords:
            if start_row <= row < end_row:
              panel_objects.append((color, coords))
              break # go to next object

        # Skip empty panels
        if not panel_objects:
            continue

        # find smallest
        smallest_object = min(panel_objects, key=lambda x: len(x[1]))
        obj_color, obj_coords = smallest_object

        # Transform color based on panel index
        if panel_index == 0:  # Top panel
            new_color = 4  # Yellow
        elif panel_index == 1:  # Middle panel
            new_color = 2  # Red
        else:  # Bottom panel
            new_color = bottom_panel_color

        for row, col in obj_coords:
            output_grid[row, col] = new_color

    return output_grid
```